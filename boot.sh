#!/bin/bash
# this script is used to boot a Docker container
source venv/bin/activate
flask deploy
exec gunicorn -b :5000 --access-logfile - --error-logfile - ZRApp:app