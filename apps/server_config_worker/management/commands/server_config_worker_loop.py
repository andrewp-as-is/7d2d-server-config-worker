from datetime import datetime
import json
import os
import asyncio
import time
from asyncio.exceptions import TimeoutError
import logging

from django.db import connection, transaction
from a2s.a2s_async import request_async
from a2s.rules import RulesProtocol

from base_apps.game_server.models import Server
from base_apps.game_server_config.models import Config, RequestError, Timestamp
from base_apps.game_server_config.utils import  get_path
from base_apps.game_server_config_request_job.models import Job
from management.base import BaseCommand

"""
https://developer.valvesoftware.com/wiki/Server_queries#A2S_RULES

https://github.com/Yepoleb/python-a2s
"""

TIMEOUT = 10
ERROR_LIST = []
RESPONSE_DATA = []
TIMESTAMP_SQL = """
INSERT INTO game_server_config_request_job.timestamp(server_id)
SELECT server_id
FROM game_server_config_request_job.job
ON CONFLICT(server_id) DO UPDATE SET
timestamp=EXCLUDED.timestamp;
""".strip()
id2addr = {s.id:s.addr for s in Server.objects.all()}
id2data = {}
id2error = {}

async def server_client(server_id):
    global id2addr, id2error, id2data
    try:
        addr = id2addr[server_id]
        addr_tuple = (addr.split(':')[0],int(addr.split(':')[1]))
        data = await request_async(addr_tuple, TIMEOUT, 'utf-8', RulesProtocol)
        id2data[server_id] = data
    except Exception as e:
        id2error[server_id] = e
        if type(e) not in (TimeoutError,):
            print('%s: %s' % (type(e),str(e)))
            logging.error(e)

async def main(loop,server_id_list):
    listen_connections = [
        loop.create_task(server_client(server_id)) for server_id in server_id_list
    ]
    await asyncio.gather(*listen_connections)

class Command(BaseCommand):
    def handle(self, *args, **options):
        global id2addr, id2data, id2error
        id2data, id2error = {}, {}
        self.execute_sql('REFRESH MATERIALIZED VIEW game_server_config_request_job.job')
        job_list = list(Job.objects.all())
        server_id_list = list(map(lambda j:j.server_id,job_list))
        self.message('%s jobs' % len(job_list))
        if not job_list:
            return self.message('SKIP: 0 jobs')
        for job in job_list:
            if job.server_id not in id2addr:
                server = Server.objects.get(id=job.server_id)
                id2addr[job.server_id] = server.addr
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop,server_id_list))
        error_objs, config_list, timestamp_list = [], [], []
        for server_id,data in id2data.items():
            """
            known issues: JsonField text vs dict
class CustomJsonField(models.JSONField):
    def from_db_value(self, value, expression, connection):
        if isinstance(value, dict):
            return value
        return super().from_db_value(value, expression, connection)
            """
            config_list.append(Config(server_id=server_id,config = data))
            timestamp_list.append(Timestamp(
                server_id=server_id,
                timestamp = int(time.time())
            ))
        for server_id,e in id2error.items():
             error_objs.append(RequestError(
                server_id=server_id,
                exc_type=str(type(e))
            ))
        cursor = connection.cursor()
        with transaction.atomic():
            RequestError.objects.bulk_create(error_objs)
            Config.objects.bulk_create(config_list,
                update_conflicts=True,
                unique_fields=['server_id'],
                update_fields=['config']
            )
            Timestamp.objects.bulk_create(timestamp_list,
                update_conflicts=True,
                unique_fields=['server_id'],
                update_fields=['timestamp']
            )
            cursor.execute(TIMESTAMP_SQL.strip())
