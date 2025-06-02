#!/bin/bash

# make sure mysql server started before anything else
# bad idea to upgrade to head this way, but i will leave it here
# you should create revision first.
#exec ./wait-for -t 30 mysql:3306 -- alembic upgrade head && echo "alembic upgrade finished!"

exec wait-for -t 30 mysql:3306 -- uvicorn main:app --host 0.0.0.0 --port 8000 --reload
