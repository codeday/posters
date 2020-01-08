#!/usr/bin/env bash

wget https://f1.srnd.org/fonts/posters.zip?v=$RANDOM -O /fonts.zip
unzip -o /fonts.zip -d /usr/share/fonts && fc-cache -f

cron -f &
uvicorn main:app --host 0.0.0.0 --port 8000
