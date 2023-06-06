import os

def get_lines(path):
    return list(filter(
        lambda s:s and '#' not in s,
        open(path).read().splitlines()
    ))

def get_context_processors():
    path = os.path.join(os.path.dirname(__file__),'context_processors.txt')
    return get_lines(path)

def get_installed_apps():
    path = os.path.join(os.path.dirname(__file__),'apps.txt')
    apps = get_lines(path)
    for root in ['apps','base_apps']:
        apps+=[
            '%s.%s' % (root,d)
            for d in next(os.walk(root))[1] if d[0].isalpha()
        ]
    return apps

def get_middleware():
    path = os.path.join(os.path.dirname(__file__),'middleware.txt')
    return get_lines(path)
