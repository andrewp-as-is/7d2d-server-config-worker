from django.db import models


class Time(models.Model):
    server_id = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    timestamp = models.IntegerField()

    UPDATE_CONFLICTS = True
    UNIQUE_FIELDS = ['server_id']

    class Meta:
        managed = False

    @classmethod
    def get_update_fields(model):
        return list(map(
            lambda f:f.name,
            filter(
                lambda f:f.name not in ['id','server_id'],
                model._meta.get_fields()
            )
        ))
