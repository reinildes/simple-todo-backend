from flask import Flask
from flask import json
from flask import Response
from flask_cors import CORS, cross_origin
from flask import request

app = Flask(__name__)
cors = CORS(app)

class Task:
    def __init__(self, desc, id, checked):
        self.desc = desc
        self.id = id
        self.checked = checked

taskList = list()

@app.route("/")
def index():
    return "Hello world, baby"

@cross_origin
@app.route("/tasks")
def tasks():
    taskListDic = list(map(lambda task: task.__dict__, taskList))
    return Response(
        json.dumps(taskListDic),
        status=200,
        mimetype='application/json')

@cross_origin
@app.route("/tasks", methods=['POST'])
def addTask():        
    data = json.loads(request.data)
    taskList.append(Task(data['desc'], data['id'], data['checked']))
    return Response(status=200)

@cross_origin
@app.route("/tasks/<int:id>", methods=['PUT'])
def updateTask(id):        
    task = list(filter(lambda task: task.id == id, taskList))[0]
    task.checked = not task.checked
    return Response(status=200)    

@cross_origin
@app.route("/tasks/<int:id>", methods=['DELETE'])
def deleteTask(id):        
    global taskList
    taskList = list(filter(lambda task: task.id != id, taskList))
    return Response(status=200)    