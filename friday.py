#!/usr/bin/python3
from ActionDatabase import ActionDatabase
import time
import subprocess as sp
from TaskQueue import TaskQueue

print("Starting Friday...")
action_db = ActionDatabase("./actions")
print("Action DB ready")

print("Starting API server")
api = sp.Popen(["./.venv/bin/flask", "run"], env={"FLASK_APP": "api.py"})
print("API ready")


def execute(task):
    print('Executing command ', task['command'])
    action_db.findAndExec(task['command'])
    return True


queue = TaskQueue()
queue.watch(execute)

while True:
    pass
