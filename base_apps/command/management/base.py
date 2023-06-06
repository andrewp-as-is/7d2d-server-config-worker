import collections
from datetime import datetime, timezone
import logging
import os
import subprocess
import sys
import time
import traceback

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection, transaction

from base_apps.command.models import CallDuration, Command,Error,Message
from base_apps.utils import print_message

COMMAND_LIST = list(Command.objects.all())

class BaseCommand(BaseCommand):

    def get_name(self):
        module_name = type(self).__module__
        app, name = module_name.split('.')[-4], module_name.split('.')[-1]
        return name

    def get_command_id(self):
        global COMMAND_LIST
        name = self.get_name()
        command = next(filter(lambda c:c.name==name,COMMAND_LIST),None)
        if not command:
            command, created = Command.objects.get_or_create(name=name)
            COMMAND_LIST.append(command)
        return command.id

    def execute(self,*args,**kwargs):
        now = datetime.now()
        started_at = int(datetime.now().timestamp())
        self.create_objs = collections.defaultdict(list)
        self.delete_objs = collections.defaultdict(list)
        self.messages = []
        try:
            self.print('%s STARTED' % self.get_name())
            self.handle(*args,**kwargs)
            td = datetime.now()-now
            self.print('%s FINISHED in %ss' % (self.get_name(),td))
        except Exception as e:
            self.message('%s: %s' % (type(e),str(e)))
            self.error(e)
        finally:
            td = datetime.now()-now
            #self.create(CallDuration(
            #    command_id=self.get_command_id(),
           # #    seconds=float('%s.%s' % (td.seconds,td.microseconds))
            #))
            if self.messages:
                self.create(Message(
                    command_id=self.get_command_id(),
                    message='\n'.join(self.messages)
                ))
            if hasattr(self,'make_transaction'):
                self.make_transaction()

    def make_transaction(self):
        with transaction.atomic():
            self.bulk_delete()
            self.bulk_create()

    def create(self,obj):
        self.create_objs[obj.__class__].append(obj)

    def delete(self,obj):
        self.delete_objs[obj.__class__].append(obj)

    def model_bulk_create(self,model,objs):
        db_table = model._meta.db_table.replace('"','')
        self.message('BULK CREATE: %s %s objects' % (db_table,len(objs)))
        update_fields = getattr(model,'update_fields',[])
        if hasattr(model,'get_update_fields'):
            update_fields =model.get_update_fields()
        model.objects.bulk_create(objs,
            update_conflicts=getattr(model,'UPDATE_CONFLICTS',False),
            unique_fields=getattr(model,'UNIQUE_FIELDS',[]),
            update_fields=update_fields
        )

    def bulk_create(self):
        for model, objs in sorted(self.create_objs.items(), key=lambda i: i[0]._meta.db_table):
            self.model_bulk_create(model, objs)
        self.create_objs = collections.defaultdict(list)

    def bulk_delete(self):
        for model, objs in sorted(self.delete_objs.items(), key=lambda i: i[0]._meta.db_table):
            pk_name = model._meta.pk.name
            db_table = model._meta.db_table.replace('"','')
            self.message('BULK DELETE: %s %s objects' % (db_table,len(objs)))
            values = list(map(lambda obj:getattr(obj,model._meta.pk.name),objs))
            model.objects.filter(**{'%s__in' % pk_name:values}).delete()
        self.delete_objs = collections.defaultdict(list)

    def call_command(self,name, *args, **options):
        call_command(name, *args, **options)

    def execute_sql(self,sql):
        if sql:
            cursor = connection.cursor()
            self.message(sql.strip())
            now = datetime.now()
            cursor.execute(sql.strip())
            td = datetime.now()-now
            self.message('FINISHED in %ss' % td)

    def message(self,message):
        # tz = datetime.now(timezone.utc).astimezone().tzinfo
        # dt = datetime.now().replace(tzinfo=tz).astimezone(tz=None)
        self.print(message)
        if message:
            if 'worker' in self.get_name():
                Message(command_id=self.get_command_id(),message=message).save()
            else:
                self.messages.append(message)

    def error(self,e):
        logging.error(e,exc_info=settings.DEBUG)
        self.message('%s: %s' % (type(e),str(e)))
        Error(
            command_id=self.get_command_id(),
            exc_type=type(e),
            exc_message=str(e),
            exc_traceback=traceback.format_exc()
        ).save()
        if settings.DEBUG:
            for i in range(0,666):
                subprocess.run(['echo','-e','"\a"'], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                os.system('/usr/bin/say "shit happens"')
                time.sleep(5)
            sys.exit(1)
        # todo: prod restart (exit 0) if connection closed
        # todo: restart on connections error/etc

    def print(self,msg):
        print_message(msg)
