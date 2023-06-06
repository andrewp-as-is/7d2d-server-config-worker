import os
import sys

from django.apps import apps
from django.db import connection
from django.template.defaultfilters import filesizeformat

from base_apps.response.models import Response
from base_apps.command.management.base import BaseCommand


SQL = """
SELECT format('%s.%s',schemaname,matviewname)
FROM pg_matviews
ORDER BY schemaname,matviewname
"""
CURSOR = connection.cursor()
CURSOR.execute(SQL)
MATVIEWS = list(map(lambda r:r[0],CURSOR.fetchall()))
SQL = """
SELECT format('%s.%s',routine_schema,routine_name)
FROM information_schema.routines
WHERE routine_type = 'PROCEDURE'
ORDER BY routine_schema,routine_name;
"""
CURSOR.execute(SQL)
PROCEDURES = list(map(lambda r:r[0],CURSOR.fetchall()))


class JobCommand(BaseCommand):
    JOB_MODEL = None

    def handle(self, *args, **options):
        # todo: matview vs table/view
        if self.get_db_table() in MATVIEWS:
            self.refresh_matview(self.get_db_table())
        self.job_list = list(self.get_jobs())
        self.message('%s: %s jobs' % (self.get_db_table(),len(self.job_list)))
        if self.job_list:
            self.init()
            self.process_job_list(self.job_list)
            self.complete()

    def get_db_schema(self):
        return self.JOB_MODEL._meta.db_table.replace('"','').split('.')[0]

    def get_db_table(self):
        return self.JOB_MODEL._meta.db_table.replace('"','')

    def make_transaction(self):
        self.bulk_delete()
        self.bulk_create()

    def get_job_queryset(self):
        return self.JOB_MODEL.objects.all()

    def get_jobs(self):
        return list(self.get_job_queryset())

    def init(self):
        pass

    def process_job_list(self,job_list):
        for job in job_list:
            try:
                self.process_job(job)
            except Exception as e:
                self.error(e)

    def process_row(self):
        raise NotImplementedError

    def make_transaction(self):
        self.bulk_delete()
        self.bulk_create()

    def complete(self):
        regproc = '%s.complete' % self.get_db_schema()
        if regproc in PROCEDURES:
            sql = 'CALL %s()' % regproc
            self.execute_sql(sql)
        else:
            self.message('SKIP: %s not found' % regproc)
