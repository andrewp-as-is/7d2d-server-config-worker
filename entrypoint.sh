#!/bin/sh

find /tmp -type f -exec rm {} \;

python -u manage.py startup
python -u manage.py worker
