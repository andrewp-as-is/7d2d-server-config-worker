from django.apps import apps

def iter_response_models():
    for model in apps.get_models():
        if model.__name__=='Response':
            yield model
