from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin

import pymongo
from bson.objectid import ObjectId
import time
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
dbclient = pymongo.MongoClient('mongodb://localhost:27017/')
taskdb = dbclient['friday_tasks']
task_queue = taskdb['task_queue']


def json_reply(reply):
    reply = jsonify(reply)
    headers = {
        'Content-Type': 'application/json'
    }
    return reply, 200, headers


@app.route('/command', methods=['POST', 'GET'])
@cross_origin()
def command():
    if request.method == 'POST':
        print('Received command')
        if not request.is_json:
            return json_reply({'status': False, 'message': 'INVALID DATA'})
        data = request.get_json()
        print(data)
        status = False
        inserted = None
        if data['command']:
            try:
                inserted = task_queue.insert_one(
                    {'command': data['command'], 'time': time.time(), 'completed': False, 'taken': False})
                status = True
            except Exception:
                print(Exception)
                status: False
        return json_reply({'status': status, 'inserted': str(inserted.inserted_id)})
    elif request.method == 'GET':
        print('Getting command status -')
        id = request.args.get('id')
        if not id:
            return json_reply({'status': False, 'message': 'INVALID DATA'})

        command = task_queue.find_one({'_id': ObjectId(id)}, {'_id': 0})
        print(command)
        completed = False
        status = True
        if not command:
            status = False
        elif ('completed' in command.keys()) and command['completed']:
            completed = True
        return json_reply({'status': status, 'command': command, 'completed': completed})


@app.route('/complete', methods=['POST', 'GET'])
def complete():
    if request.method == 'POST':
        data = request.get_json()
        id = data['id']
        result = data['result']
        try:
            task_queue.update_one({'_id': ObjectId(id)}, {
                '$set': {'completed': True, 'result': result}})
            return json_reply(
                {'status': True, 'message': 'SUCCESS'})
        except Exception as e:
            print(e)
            return json_reply(
                {'status': False, 'message': 'ERROR'})
    else:
        id = request.args.get('id')
        try:
            result = task_queue.find_one(
                {'_id': ObjectId(id), 'completed': True})
            if not result:
                return json_reply(
                    {'status': False, 'message': 'NO COMPLETED TASKS'})
            print('deleting id - ', id)
            task_queue.delete_one(
                {'_id': ObjectId(id), 'completed': True})
            return json_reply(
                {'status': True, 'result': result['result'], 'command': result['command']})
        except Exception as e:
            print(e)
            return json_reply(
                {'status': False, 'message': 'ERROR'})


@app.route('/')
def index():
    return 'Friday!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
