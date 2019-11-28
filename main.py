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

usersData = dict()

@app.route("/users", methods=['POST'])
def newUser():
    data = json.loads(request.data)
    
    if usersData.get(data['user']) == None:
        usersData[data['user']] = list()
    return Response(status=201)  

@cross_origin
@app.route("/tasks/<user>")
def tasks(user):
    taskListDic = list(map(lambda task: task.__dict__, usersData.get(user)))
    return Response(
        json.dumps(taskListDic),
        status=200,
        mimetype='application/json')

@cross_origin
@app.route("/tasks/<user>", methods=['POST'])
def addTask(user):        
    data = json.loads(request.data)
    usersData.get(user).append(Task(data['desc'], data['id'], data['checked']))
    return Response(status=201)

@cross_origin
@app.route("/tasks/<user>/<int:id>", methods=['PUT'])
def updateTask(user, id):        
    task = list(filter(lambda task: task.id == id, usersData.get(user)))[0]
    task.checked = not task.checked
    return Response(status=200)    

@cross_origin
@app.route("/tasks/<user>/<int:id>", methods=['DELETE'])
def deleteTask(user, id):        
    global usersData
    usersData[user] = list(filter(lambda task: task.id != id, usersData.get(user)))
    return Response(status=200)    

@app.after_request
def addHeader(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)    