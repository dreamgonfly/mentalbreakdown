#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import Task
from datetime import datetime, timedelta

from app.parse import parse_todo

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

    def test_parse(self):
        t1 = Task(raw = 'Buy milk')
        db.session.add(t1)
        db.session.commit()
        assert t1.todo == 'Buy milk'
        t2 = Task(raw = 'Buy milk (2)')
        db.session.add(t2)
        db.session.commit()
        assert t2.todo == 'Buy milk'
        assert t2.required_time == 2
        t1 = parse_todo('Buy milk')
        assert t1['todo'] == 'Buy milk'
        t2 = parse_todo('Buy milk (2)')
        assert t2['todo'] == 'Buy milk'
        assert t2['required_time'] == 2
        p = parse_todo('Buy milk (2) ~2015-3-25 14:35:24')
        assert p['todo'] == 'Buy milk'
        assert p['required_time'] == 2
        assert p['due'] == datetime(2015, 3, 25, 14, 35, 24)
        p = parse_todo('Buy milk (2) ~4:35')
        assert p['todo'] == 'Buy milk'
        assert p['required_time'] == 2
        assert p['due'].year == datetime.today().year
        assert p['due'].month == datetime.today().month
        assert p['due'].day == datetime.today().day
        assert p['due'].hour == 4
        assert p['due'].minute == 35
        p = parse_todo('Buy milk ~3-25 (2)')
        assert p['todo'] == 'Buy milk'
        assert p['required_time'] == 2
        assert p['due'].year == datetime.today().year
        assert p['due'].month == 3
        assert p['due'].day == 25
        assert p['due'].hour == 23
        assert p['due'].minute == 59
        p = parse_todo('Buy milk (2) ~3-25 14:35')
        assert p['todo'] == 'Buy milk'
        assert p['required_time'] == 2
        assert p['due'].year == datetime.today().year
        assert p['due'].month == 3
        assert p['due'].day == 25
        assert p['due'].hour == 14
        assert p['due'].minute == 35
        p = parse_todo('Buy milk ~4h')
        assert p['todo'] == 'Buy milk'
        assert p['due'].year == datetime.today().year
        assert p['due'].month == datetime.today().month
        assert p['due'].day == datetime.today().day
        assert p['due'].hour == datetime.today().hour + 4
        p = parse_todo('Buy milk ~2d (2)')
        assert p['todo'] == 'Buy milk'
        assert p['due'].year == datetime.today().year
        assert p['due'].month == datetime.today().month
        assert p['due'].day == datetime.today().day + 2
        assert p['due'].hour == 23
        assert p['due'].minute == 59

if __name__ == '__main__':
    unittest.main()