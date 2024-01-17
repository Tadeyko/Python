from .base import Base
from extensions import db
from app.tasks.models import Todo

class Tasks(Base):
    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create(self):
        response = self.client.post('/tasks', data=dict(title='test1'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test1', response.data)

    def test_read(self):
        task = Todo(title='test2', complete=False)
        db.session.add(task)
        db.session.commit()
        response = self.client.get('/tasks/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test2', response.data)

    def test_update(self):
        task = Todo(title='test3', complete=False)
        db.session.add(task)
        db.session.commit()
        response = self.client.get(f'/tasks/update/{task.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        task = Todo(title='test4', complete=False)
        db.session.add(task)
        db.session.commit()
        response = self.client.get(f'/tasks/delete/{task.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'test4', response.data)    