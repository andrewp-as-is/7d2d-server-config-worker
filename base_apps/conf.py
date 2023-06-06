import os

# /Volumes/1TB-SEAGATE-SLIM/.7d2d.com/files
ROOT_DIRNAME = os.path.join('/Volumes/HDD','.7d2d.com','files')
if os.path.exists('/.dockerenv'): # docker container
    ROOT_DIRNAME = os.path.join('/files') # use docker volumes
