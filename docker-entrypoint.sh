#!/usr/bin/env bash
cron -f &
uvicorn main:app --host 0.0.0.0 --port 8000
