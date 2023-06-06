from django.conf import settings
from django.db import models
from django_passwordless_user.models import AbstractBaseUser


class UserMixin:

    def get_absolute_url(self):
        return '/u/%s/' % self.login

    def get_avatar_url(self):
        return 'https://github.com/%s.png' % (self.login,)


class User(AbstractBaseUser):
    last_login = models.DateTimeField(blank=True, null=True)
    # steam real login unknown

    personaname = models.TextField(unique=False)
    avatar = models.TextField(null=True)
    avatarmedium = models.TextField(null=True)
    avatarfull = models.TextField(null=True)
    loccountrycode = models.TextField(null=True)

    USERNAME_FIELD = 'personaname'
    is_active = True
    is_anonymous = False
    is_authenticated = True

    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = '%s\".\"%s' % ('steam','user')

    def get_absolute_url(self):
        pass
        # return '/u/%s/' % self.login

    #def get_avatar_url(self):
    #    return 'https://github.com/%s.png' % (self.login,)

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False
