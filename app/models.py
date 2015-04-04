from app import db
from datetime import datetime
from .parse import parse_todo
from .prioritize import pick_one

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    raw = db.Column(db.String(140))
    todo = db.Column(db.String(100))
    required_time = db.Column(db.Integer, default = 1)
    scheduled = db.Column(db.DateTime)
    due = db.Column(db.DateTime)
    completed_time = db.Column(db.DateTime)
    dropped_time = db.Column(db.DateTime)
    last_notnow = db.Column(db.DateTime)
    number_of_notnow = db.Column(db.Integer, default = 0)
    
    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        r = parse_todo(kwargs['raw'])
        self.todo = r['todo']
        if 'required_time' in r:
            self.required_time = r['required_time']
        else:
            self.required_time = 1
        if 'due' in r:
            self.due = r['due']
        self.last_notnow = datetime.min
        self.timestamp = datetime.now()

    def edit(self, raw):
        self.raw = raw
        r = parse_todo(raw)
        self.todo = r['todo']
        if 'required_time' in r:
            self.required_time = r['required_time']
        else:
            self.required_time = 1
        if 'due' in r:
            self.due = r['due']

    def __repr__(self):
        return '<Task {}>'.format(self.raw)

    @staticmethod
    def active_tasks():
    	return Task.query.filter_by(completed_time = None).filter_by(dropped_time = None)

    @staticmethod
    def pick_one():
    	return pick_one(Task.active_tasks().all())