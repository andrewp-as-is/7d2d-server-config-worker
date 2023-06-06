from django.apps import apps
from django.db.models.signals import class_prepared, pre_init

"""
1) models.py
apps/schemaname/models.py
class Tablename(models.Model)
2) models/
apps/schemaname/models/__init__.py
apps/schemaname/models/tablename.py
"""


def set_db_table(sender, **kwargs):
    try:
        config = apps.get_app_config(sender._meta.app_label)
    except LookupError as e:
        pass
    if 'apps' in sender.__module__ or 'base_apps' in sender.__module__:
        db_schema = sender._meta.app_label
        if sender.__module__.split('.')[-1]=='models': # models.py
            db_table = '%s\".\"%s' % (db_schema,sender.__name__.lower())
        else: # models/
            db_table = '%s\".\"%s' % (db_schema,sender.__module__.split('.')[-1])
        sender._meta.db_table = db_table

pre_init.connect(set_db_table)
class_prepared.connect(set_db_table)
