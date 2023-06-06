from django.core.management import get_commands
from django.db import connection
from management.base import BaseCommand
from .utils import iter_response_models

"""
response.response TABLE

domain_xxx_response.response (...,object_id,job) MATVIEW
domain_xxx_response.timestamp (object_id,timestamp)

domain_xxx_response_job.job (response_id) MATVIEW
"""

SQL = """
SELECT t.table_schema,c.column_name
FROM information_schema.table_constraints AS t
INNER JOIN information_schema.constraint_column_usage AS c
    ON t.constraint_name = c.constraint_name
    AND c.constraint_schema = t.table_schema
WHERE
t.table_schema LIKE '%_response' AND
t.table_name='timestamp' AND
t.constraint_type IN ('PRIMARY KEY');
"""
CURSOR = connection.cursor()
CURSOR.execute(SQL)
PRIMARY_KEYS = {r[0]:r[1] for r in CURSOR.fetchall()}

# todo: size
# todo: delete where job=false
# todo: save response? not delete/etc

class ResponseCommand(BaseCommand):
    DELETE_RESPONSE = True # todo

    def handle(self, *args, **options):
        db_schema = self.get_name()
        self.refresh_matview('%s.response' % db_schema)
        if db_schema in PRIMARY_KEYS:
            primary_key = PRIMARY_KEYS[db_schema]
            self.refresh_matview('%s.response' % db_schema)
            sql = """INSERT INTO {db_schema}.timestamp({primary_key},timestamp)
SELECT {primary_key},extract(epoch FROM (now()))
FROM {db_schema}.response
ON CONFLICT({primary_key}) DO UPDATE SET
timestamp=EXCLUDED.timestamp
WHERE timestamp.timestamp IS DISTINCT FROM EXCLUDED.timestamp;
""".format(db_schema=db_schema,primary_key=primary_key)
            self.execute_sql(sql)
        if self.DELETE_RESPONSE:
            sql = """DELETE FROM response.response
    WHERE id IN (SELECT id FROM %s.response WHERE job=false)
            """ % db_schema
            self.execute_sql(sql)
            # todo: VACUUM xxx_response.timestamp
        job = '%s_job' % self.get_name()
        if job in get_commands():
            Response = self.get_response_model()
            jobs_count = Response.objects.filter(job=True).count()
            self.message('%s.response: %s jobs' % (db_schema,jobs_count))
            if jobs_count:
                self.call_command(job)
        self.execute_sql('VACUUM %s.timestamp' % db_schema)

    def get_response_model(self):
        for model in iter_response_models():
            db_schema = model._meta.db_table.split('.')[0].replace('"','')
            if db_schema==self.get_name():
                return model
        return Response
