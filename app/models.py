from app import db
from datetime import datetime
import re
from random import choice

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    raw = db.Column(db.String(140))
    todo = db.Column(db.String(100))
    estimated_time = db.Column(db.Integer, default = 1)
    due = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default = False)

    def __init__(self, *args, **kwargs):
    	db.Model.__init__(self, *args, **kwargs)
    	pattern = re.compile(r'(?P<todo>[\w\s,\.]+)(?:\((?P<estimated_time>\d+)\))?')
    	r = pattern.match(kwargs['raw']).groupdict()
    	self.todo = r['todo'].strip()
    	if r['estimated_time']:
	    	self.estimated_time = int(r['estimated_time'])
    	self.timestamp = datetime.now()

    def __repr__(self):
        return '<Task {}>'.format(self.raw)

    @staticmethod
    def active_tasks():
    	return Task.query.filter_by(completed = False)

    @staticmethod
    def pick_one():
    	candidates = Task.active_tasks().order_by(Task.estimated_time)
    	first_group = candidates.filter_by(estimated_time = candidates.first().estimated_time)
    	return choice(first_group.all())