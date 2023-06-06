from django.db import models


class Server(models.Model):
    addr = models.TextField(unique=True)
    ip = models.TextField()
    port = models.IntegerField()

    # game_server.steam_info - steam server info
    steam_info_name = models.TextField()
    steam_info_version = models.TextField()
    steam_info_max_players_count = models.IntegerField()
    steam_info_players_count = models.IntegerField()
    steam_info_map = models.TextField()
    uptodate = models.BooleanField()
    pvp = models.BooleanField()

    discord_url = models.TextField() # config parsed
    homepage_url = models.TextField() # config parsed
    country = models.TextField() # server ip -> country
    time = models.IntegerField() # "CurrentTime"
    day = models.IntegerField() # "CurrentTime" day number

    # config
    IsPasswordProtected = models.BooleanField()
    DayLightLength = models.IntegerField()
    DayNightLength = models.IntegerField()
    DropOnDeath = models.IntegerField()
    DropOnQuit = models.IntegerField()
    GameDifficulty = models.IntegerField()
    Language = models.TextField()
    Region = models.TextField()
    ServerDescription = models.TextField()
    ServerVersion = models.TextField()
    XPMultiplier = models.IntegerField()
    WorldSize = models.IntegerField()

    class Meta:
        managed = False
