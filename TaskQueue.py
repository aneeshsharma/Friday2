import pymongo
import time


class TaskQueue:
    def __init__(self):
        dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
        taskdb = dbclient['friday_tasks']
        self.task_queue_db = taskdb['task_queue']

    def watch(self, execute):
        if not execute:
            print('No execution function found')
            return
        while True:
            try:
                doc = self.task_queue_db.find({'taken': False})
                for x in doc:
                    self.task_queue_db.update_one(
                        {'_id': x['_id']}, {'$set': {'taken': True}})
                    execute(x)
            except Exception as e:
                print(e)
                break
            time.sleep(0.1)
