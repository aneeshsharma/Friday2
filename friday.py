#!/usr/bin/python3
from ActionDatabase import ActionDatabase
import time

action_db = ActionDatabase("./actions")

action_db.findAndExec("ping")
