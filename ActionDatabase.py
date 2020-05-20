import os
import json
import re
import subprocess


class ActionDatabase:
    def __init__(self, action_dir):
        self.action_dir = action_dir
        self.actions = []
        actions = os.listdir(action_dir)
        count = len(actions)
        print("Loading actions...")
        for i in range(count):
            action = actions[i]
            print(str(i+1) + " of " + str(count), end="\r")
            config_file = open(action_dir + "/" + action + "/config.json")
            config = json.load(config_file)
            self.actions.append({"dir": action, "config": config})
            config_file.close()

    def findTask(self, command):
        for action in self.actions:
            if re.match(action["config"]["regex"], command):
                print("Found match - ", action["config"]["name"])
                return action
        return None

    def findAndExec(self, command, id):
        action = self.findTask(command)
        if not action:
            return False
        wd = self.action_dir + "/" + action["dir"]
        process = subprocess.Popen(
            ["python3", action["config"]["exec"]], cwd=wd, env={**os.environ, 'TASK_ID': id})
        return process
