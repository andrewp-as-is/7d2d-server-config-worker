import os
import sys

from django.apps import apps
from django.template.defaultfilters import filesizeformat

from base_apps.response.models import Response
from management.job.base import JobCommand
from .utils import iter_response_models

"""
domain_xxx_response.response
domain_xxx_response_job.job (response_id)
"""

def iter_response_models():
    for model in apps.get_models():
        if model.__name__=='Response':
            yield model

class ResponseJobCommand(JobCommand):
    # RESPONSE_MODEL = Response # get_response_model
    DELETE_RESPONSE = True
    DELETE_FILES = False


    def handle(self, *args, **options):
        self.refresh_matview(self.get_db_table())
        self.response_list = list(self.get_response_queryset())
        self.message('%s: %s responses' % (self.get_db_table(),len(self.response_list)))
        if self.response_list:
            self.init()
            self.process_response_list(self.response_list)
            self.complete()

    def get_response_model(self):
        for model in iter_response_models():
            db_schema = model._meta.db_table.split('.')[0].replace('"','')
            if db_schema+'_job'==self.get_name():
                return model
        return Response

    def get_response_queryset(self):
        return self.get_response_model().objects.filter(
            id__in=self.JOB_MODEL.objects.values_list('response_id',flat=True)
        )

    def process_response_list(self,response_list):
        for response in response_list:
            try:
                self.process_response(response)
            except Exception as e:
                self.error(e)

    def process_response(self,response):
        method_name = 'process_%s_response' % response.status
        # пересоздавать автоматически опасно. возможно и не нужно
        # self.message('%s status %s' % (response.url,response.status))
        if response.status==200:
            full_filepath = response.get_full_filepath()
            # self.message('%s path %s' % (response.url,path))
            if full_filepath:
                if not os.path.exists(full_filepath):
                    return self.message('%s\n%s NOT EXISTS' % (response.url,full_filepath))
                if not os.path.getsize(full_filepath):
                    return self.message('%s\n%s EMPTY' % (response.url,full_filepath))
                size = os.path.getsize(full_filepath)
                self.message('%s size %s' % (full_filepath,filesizeformat(size)))
        if hasattr(self,method_name):
            getattr(self,method_name)(response)
        else:
            self.message('%s NOT IMPLEMENTED' % method_name)

    def make_transaction(self):
        self.bulk_delete()
        self.bulk_create()
        # todo: domain.response?
        if self.DELETE_RESPONSE:
            Response.objects.filter(
                id__in=self.JOB_MODEL.objects.values_list('response_id',flat=True)
            ).delete()

    def complete(self):
        self.delete_files()
        Response.objects.filter(
            id__in=self.JOB_MODEL.objects.values_list('response_id',flat=True)
        ).delete()

    def delete_files(self):
        count = 0
        for response in filter(lambda r:r.filepath,self.response_list):
            path = response.get_full_filepath()
            if path:
                if os.path.exists(path):
                    try:
                        os.unlink(path)
                        count+=1
                    except Exception as e:
                        logging.error(e)
        if count:
            self.message('DELETED %s files' % count)

    def get_project_id(self):
        return self.get_response_queryset().values_list('project_id',flat=True)

    def get_release_id(self):
        return self.get_response_queryset().values_list('release_id',flat=True)

    def get_repo_id(self):
        return self.get_response_queryset().values_list('repo_id',flat=True)

    def get_user_id(self):
        return self.get_response_queryset().values_list('user_id',flat=True)

