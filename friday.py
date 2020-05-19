#!/usr/bin/python3
from ActionDatabase import ActionDatabase
import time
import subprocess as sp

print("Starting Friday...")
action_db = ActionDatabase("./actions")
print("Action DB ready")

print("Starting API server")
api = sp.Popen(["./.venv/bin/flask", "run"], env={"FLASK_APP": "api.py"})
print("API ready")

while True:
    pass
