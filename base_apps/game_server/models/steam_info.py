from django.db import models


class SteamInfo(models.Model):
    server = models.ForeignKey('server', related_name="+", on_delete=models.CASCADE,primary_key=True)
    name = models.TextField(null=True)
    version = models.TextField(null=True)
    uptodate = models.BooleanField()
    max_players = models.IntegerField(null=True)
    players = models.IntegerField(null=True)
    map = models.TextField(null=True)

    UPDATE_CONFLICTS = True
    UNIQUE_FIELDS = ['server_id']
    UPDATE_FIELDS = ['name','version','players','max_players','map','uptodate',]

    class Meta:
        managed = False

    @classmethod
    def get_update_fields(model):
        return model.UPDATE_FIELDS
