#!/usr/bin/python3
from ActionDatabase import ActionDatabase
import time
import subprocess as sp
import os
from TaskQueue import TaskQueue

print("Starting Friday...")
action_db = ActionDatabase("./actions")
print("Action DB ready")

print("Starting API server")
api = sp.Popen(["python3", "api.py"], cwd='.')
print("API ready")


def execute(task):
    print('Executing command ', task['command'])
    process = action_db.findAndExec(task['command'], str(task['id']))
    if not process:
        return False
    else:
        return True


queue = TaskQueue()
queue.watch(execute)

while True:
    pass
