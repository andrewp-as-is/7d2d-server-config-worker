import os
from ..conf import ROOT_DIRNAME

CONFIG_DIRNAME = os.path.join(ROOT_DIRNAME)
if not os.path.exists(CONFIG_DIRNAME):
    os.makedirs(CONFIG_DIRNAME)

def get_path(addr):
    return os.path.join(ROOT_DIRNAME,'servers',addr,'config.json')
