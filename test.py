import unittest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from main import app, db, Task


class FlaskAppTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.client = None

    def setUp(self):
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        self.client = self.app

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.app.post('/tasks', json={'title': 'New Task'})
        self.assertEqual(response.status_code, 201)

    def test_get_task(self):
        task = Task(title='Test Task', description='Test Description', done=False)

        with app.app_context():
            db.session.add(task)
            db.session.commit()

            response = self.app.get(f'/tasks/{task.id}')
            self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['title'], 'Test Task')

    def test_update_task(self):
        with app.app_context():
            task_id = self.create_task('Task to Update')

            task = Task.query.get(task_id)

            response = self.client.put(f'/tasks/{task_id}', json={
                'title': 'Updated Task',
                'description': 'Updated Description',
                'done': True
            })
            self.assertEqual(response.status_code, 200)

            updated_task = Task.query.get(task_id)
            self.assertEqual(updated_task.title, 'Updated Task')
            self.assertEqual(updated_task.description, 'Updated Description')
            self.assertTrue(updated_task.done)

    def create_task(self, title):
        with app.app_context():
            new_task = Task(title=title)
            db.session.add(new_task)
            db.session.commit()
            return new_task.id

    def test_delete_task(self):
        with app.app_context():
            task_id = self.create_task('Task to Delete')

            task = Task.query.get(task_id)

            response = self.client.delete(f'/tasks/{task_id}')
            self.assertEqual(response.status_code, 204)

            deleted_task = Task.query.get(task_id)
            self.assertIsNone(deleted_task)


if __name__ == '__main__':
    unittest.main()
