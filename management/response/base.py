from django.core.management import get_commands
from django.db import connection
from base_apps.response.models import Response
from management.base import BaseCommand
from .utils import iter_response_models

"""
response.response TABLE

domain_xxx_response.response (...,object_id,job) MATVIEW
domain_xxx_response.timestamp (object_id,timestamp)

domain_xxx_response_job.job (response_id) MATVIEW
"""

SQL = """
SELECT format('%s.%s',routine_schema,routine_name)
FROM information_schema.routines
WHERE routine_type = 'PROCEDURE';
"""
CURSOR = connection.cursor()
CURSOR.execute(SQL)
PROCEDURES = list(CURSOR.fetchall())

class ResponseCommand(BaseCommand):
    DELETE_RESPONSE = True

    def handle(self, *args, **options):
        db_schema = self.get_name()
        self.refresh_matview('%s.response' % db_schema)
        for name in ['save','delete']:
            regproc = '%s.%s' % (db_schema,name)
            sql = 'CALL %s()' % regproc
            self.execute_sql(sql)
        job = '%s_job' % self.get_name()
        if job in get_commands():
            model = self.get_response_model()
            jobs_count = model.objects.filter(job=True).count()
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
