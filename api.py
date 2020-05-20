from flask import Flask, request, make_response
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


@app.route('/command', methods=['POST', 'GET'])
@cross_origin()
def command():
    if request.method == 'POST':
        print('Received command')
        if not request.is_json:
            response = make_response(
                {'status': False, 'message': 'INVALID DATA'})
            response.headers['Content-Type'] = 'application/json'
            return response
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
        response = make_response(
            {'status': status, 'inserted': str(inserted.inserted_id)})
        response.headers['Content-Type'] = 'application/json'
        return response
    elif request.method == 'GET':
        print('Getting command status -')
        id = request.args.get('id')
        if not id:
            response = make_response(
                {'status': False, 'message': 'INVALID DATA'})
            response.headers['Content-Type'] = 'application/json'
            return response

        command = task_queue.find_one({'_id': ObjectId(id)}, {'_id': 0})
        print(command)
        completed = False
        status = True
        if not command:
            status = False
        elif ('completed' in command.keys()) and command['completed']:
            completed = True
        response = make_response(
            {'status': status, 'command': command, 'completed': completed})
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/complete', methods=['POST', 'GET'])
def complete():
    if request.method == 'POST':
        data = request.get_json()
        id = data['id']
        result = data['result']
        try:
            task_queue.update_one({'_id': ObjectId(id)}, {
                '$set': {'completed': True, 'result': result}})
            response = make_response(
                {'status': True, 'message': 'SUCCESS'})
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            print(e)
            response = make_response(
                {'status': False, 'message': 'ERROR'})
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        id = request.args.get('id')
        try:
            result = task_queue.find_one(
                {'_id': ObjectId(id), 'completed': True})
            if not result:
                response = make_response(
                    {'status': False, 'message': 'NO COMPLETED TASKS'})
                response.headers['Content-Type'] = 'application/json'
                return response
            print('deleting id - ', id)
            task_queue.delete_one(
                {'_id': ObjectId(id), 'completed': True})
            response = make_response(
                {'status': True, 'result': result['result'], 'command': result['command']})
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            print(e)
            response = make_response(
                {'status': False, 'message': 'ERROR'})
            response.headers['Content-Type'] = 'application/json'
            return response


@app.route('/')
def index():
    return 'Friday!'
