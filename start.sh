#!/bin/bash

python /app/main.py
echo -e "$CRONTIME $USER python /app/main.py 2>&1\n#empty line" >/etc/cron.d/mycron
crontab /etc/cron.d/mycron
cron && tail -f /app/AutoScripts.log