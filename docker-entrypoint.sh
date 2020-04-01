#!/usr/bin/env bash

wget https://f1.srnd.org/fonts/posters.zip?v=$RANDOM -O /fonts.zip >/dev/null 2>&1
unzip -o /fonts.zip -d /usr/share/fonts >/dev/null 2>&1
fc-cache -f > /dev/null 2>&1

uvicorn main:app --host 0.0.0.0 --port 8000 --no-access-log
