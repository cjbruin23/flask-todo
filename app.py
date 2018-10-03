from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

todos = {}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in todos:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class TodoList(Resource):
    def get(self):
        return todos

    def post(self):
        args = parser.parse_args()
        try:
            todo_id = int(max(todos.keys()).lstrip('todo')) + 1
        except:
            todo_id = 1
        todo_id = 'todo%i' % todo_id
        todos[todo_id] = args['task']
        response = "Added to todos: {}".format(args['task'])
        return response, 201


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        todos[todo_id] = request.form['task']
        return {todo_id: todos[todo_id]}

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del todos[todo_id]
        return todos, 200

api.add_resource(TodoList, '/')
api.add_resource(Todo, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
