import time
import requests
import os

id = os.environ['TASK_ID']
print('Task id -', id)
start = time.time()
for i in range(5):
    print("Pong", (i+1))
    time.sleep(1)
print('Completed ', (time.time() - start))

result = {'text': 'pong'}
requests.post('http://localhost:5000/complete',
              json={'id': id, 'result': result})
