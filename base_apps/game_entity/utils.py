from .models import Entity

ID2KEY = {}
KEY2ID = {}
for e in Entity.objects.all():
    ID2KEY[e.id] = e.key
    KEY2ID[e.key] = e.id

def get_key(entity_id):
    return ID2KEY.get(entity_id,None)

def get_id(key):
    return KEY2ID.get(key,None)
