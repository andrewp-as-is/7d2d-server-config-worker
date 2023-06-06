import os
from ..conf import ROOT_DIRNAME

CONFIG_DIRNAME = os.path.join(ROOT_DIRNAME,'config')
if not os.path.exists(CONFIG_DIRNAME):
    os.makedirs(CONFIG_DIRNAME)

def get_config_path(server_id):
    return os.path.join(CONFIG_DIRNAME,str(server_id))
