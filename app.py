from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

todos = {
    "todo1": "Buy Milk"
}

def abort_if_todo_exists(todo_id):
    if todo_id in todos:
        abort(404, message="Todo {} already exist".format(todo_id))

def abort_if_todo_doesnt_exist(todo_id):
    print(todos)
    if todo_id not in todos:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class TodoList(Resource):
    def get(self):
        return todos

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(todos.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        todos[todo_id] = args['task']
        return todos, 201


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        todos[todo_id] = request.form['task']
        return {todo_id: todos[todo_id]}


api.add_resource(TodoList, '/')
api.add_resource(Todo, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
