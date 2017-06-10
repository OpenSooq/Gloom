#!/bin/bash
cd /app/

#Create
CONFD_OPTIONS=${CONFD_OPTIONS:-"-onetime -backend=env"}
/usr/local/bin/confd -log-level=debug $CONFD_OPTIONS -confdir=$PWD/confd

cd /app/code/ && source virtualenv/bin/activate 

# Update the code to the latest version
git fetch origin && git checkout -f master && git pull origin master

command="$1" ; shift
case "$command" in
  bash)
    exec /bin/bash 
    ;;
  migrate)
    exec python ./cli.py migrate
    ;;
  *)
    exec uwsgi --http-socket 0.0.0.0:3000 ./uwsgi.ini 
    ;;
esac
