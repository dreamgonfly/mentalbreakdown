#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import Task


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_make_task(self):
        t1 = Task(raw = 'Buy milk')
        db.session.add(t1)
        db.session.commit()
        assert t1.todo == 'Buy milk'
        assert t1.estimated_time == 1
        t2 = Task(raw = 'Buy milk (2)')
        db.session.add(t2)
        db.session.commit()
        assert t2.todo == 'Buy milk'
        assert t2.estimated_time == 2

if __name__ == '__main__':
    unittest.main()