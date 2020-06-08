import pymongo
import time
import requests


class TaskQueue:
    def __init__(self):
        dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
        taskdb = dbclient['friday_tasks']
        self.task_queue_db = taskdb['task_queue']

    def watch(self, execute):
        time.sleep(5)
        if not execute:
            print('No execution function found')
            return
        while True:
            try:
                tasks = requests.get('http://localhost:5000/tasks').json()
                for x in tasks:
                    if not execute(x):
                        requests.post(
                            'http://localhost:5000/complete?id=' + str(x['id']))
            except Exception as e:
                print(e)
                break
            time.sleep(0.1)
