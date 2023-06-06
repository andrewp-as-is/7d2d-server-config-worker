from datetime import datetime, timezone

from django.conf import settings

def print_message(msg):
    # todo: database?
    if settings.DEBUG:
        tz = datetime.now(timezone.utc).astimezone().tzinfo
        dt = datetime.now().replace(tzinfo=tz).astimezone(tz=None)
        # todo: django already inited timezone
        print('[%s] %s' % (dt.strftime('%H:%M:%S'),msg))


def get_timestamp():
    return int(datetime.now().timestamp())

def getfield(site):
    return 'is_' + site.domain.replace('api.', '').replace('m.', '').replace('-', '_').replace('42', '').split('.')[0]

def getsite(request):
    if settings.SITE_ID:
        return list(filter(lambda site: site.pk == settings.SITE_ID, SITE_LIST))[0]
    host = request.get_host().replace('m.', '').replace('api.', '')
    for site in SITE_LIST:
        if site.domain == host:
            return site
    return list(filter(lambda site: site.pk == 1, SITE_LIST))[0]
