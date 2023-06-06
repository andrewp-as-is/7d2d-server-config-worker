from base_apps.game_entity.utils import get_key
from .models import Translation

TEXT2KEY = {}
for translation in Translation.objects.all():
    key = get_key(translation.entity_id)
    TEXT2KEY[translation.text] = key

def get_code(name):
    if name.lower() in ['russsian']:
        return 'ru'
    return '' # default (english)

def get_key(text):
    return TEXT2KEY.get(text,None)
