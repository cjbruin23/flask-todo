from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import datetime

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('due_date')
parser.add_argument('completed')

todos = {}

def abort_if_todo_doesnt_exist(todo_id):
    if int(todo_id) not in todos.keys():
        abort(404, message="Todo {} doesn't exist".format(todo_id))

def create_new_todo_dict(title, due_date):
    new_todo = {}
    date_now = datetime.datetime.today().strftime('%m-%d-%Y')

    todos_keys = [*todos]
    next_id = next(i for i, e in enumerate(sorted(todos_keys) + [ None ], 1) if i != e)

    new_todo['title'] = title
    new_todo['creation'] = date_now
    new_todo['due_date'] = due_date
    new_todo['completed'] = False
    new_todo['completion_date'] = None

    return next_id, new_todo


class TodoList(Resource):
    def get(self):
        return todos

    def post(self):
        args = parser.parse_args()
        next_id, new_todo = create_new_todo_dict(args['title'], args['due_date'])
        todos[next_id] = new_todo
        return new_todo, 201


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        args = parser.parse_args()
        for key, value in args.items():
            # print(key, value)
            if value == '':
                continue
            else:
                todos[todo_id][key] = value

        return {todo_id: todos[todo_id]}, 200

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del todos[todo_id]
        return todos, 200

api.add_resource(TodoList, '/')
api.add_resource(Todo, '/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
