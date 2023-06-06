#!/usr/bin/open -a Terminal
{ set +x; } 2>/dev/null

{ set -x; cd "${0%/*/*}"; { set +x; } 2>/dev/null; }

[ -e .env ] && { set -o allexport; . .env || exit; }

( set -x; python -u manage.py server_config_worker_loop )
