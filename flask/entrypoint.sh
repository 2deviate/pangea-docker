#!/bin/sh -e

case $1 in

  server)
    sudo -E /usr/sbin/crond -f -l 0 -L /var/log/cron.log &
    gunicorn --workers 5 -t 60 -b 0.0.0.0:8000 wsgi:app
  ;;

  cron)
    exec /usr/sbin/crond -f    
  ;;

  *)
    exec "$@"
  ;;

esac

exit 0