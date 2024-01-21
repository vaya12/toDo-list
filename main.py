from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
ma = Marshmallow(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    done = db.Column(db.Boolean, default=False)


class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    done = ma.auto_field()


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# API endpoints
class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task_schema.dump(task)

    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str)
        parser.add_argument('done', type=bool, default=False)
        data = parser.parse_args()

        task.title = data['title']
        task.description = data['description']
        task.done = data['done']
        db.session.commit()
        return task_schema.dump(task)

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204


class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str)
        parser.add_argument('done', type=bool, default=False)
        data = parser.parse_args()

        new_task = Task(title=data['title'], description=data['description'], done=data['done'])
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Task API"
    }
)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
