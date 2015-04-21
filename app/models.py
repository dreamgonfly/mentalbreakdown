from app import db
from datetime import datetime
from .parse import parse_todo
from .prioritize import pick_one
from sqlalchemy.sql.expression import or_  

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
        parsed = parse_todo(kwargs['raw'])
        self.todo = parsed['todo']
        if 'required_time' in parsed:
            self.required_time = parsed['required_time']
        else:
            self.required_time = 1
        if 'scheduled' in parsed:
            self.scheduled = parsed['scheduled']
        if 'due' in parsed:
            self.due = parsed['due']
        self.last_notnow = datetime.min
        self.timestamp = datetime.now()
        self.raw = self.todo + (' (' + str(self.required_time) + ')' if 'required_time' in parsed else '') + \
            (' ' if 'scheduled' in parsed or 'due' in parsed else '') + \
            (str(self.scheduled) if 'scheduled' in parsed else '') + \
            ('~' if 'scheduled' in parsed or 'due' in parsed else '') + \
            (str(self.due) if 'due' in parsed else '')


    def edit(self, raw):
        parsed = parse_todo(raw)
        self.todo = parsed['todo']
        if 'required_time' in parsed:
            self.required_time = parsed['required_time']
        else:
            self.required_time = 1
        if 'scheduled' in parsed:
            self.scheduled = parsed['scheduled']
        if 'due' in parsed:
            self.due = parsed['due']
        else:
            self.due = None
        self.raw = self.todo + (' (' + str(self.required_time) + ')' if 'required_time' in parsed else '') + \
            (' ' if 'scheduled' in parsed or 'due' in parsed else '') + \
            (str(self.scheduled) if 'scheduled' in parsed else '') + \
            ('~' if 'scheduled' in parsed or 'due' in parsed else '') + \
            (str(self.due) if 'due' in parsed else '')


    def __repr__(self):
        return '<Task {}>'.format(self.raw)

    @staticmethod
    def active_tasks():
        return Task.query.filter_by(completed_time = None).filter_by(dropped_time = None).filter(or_(Task.scheduled == None, Task.scheduled < datetime.now()))

    @staticmethod
    def pick_one():
    	return pick_one(Task.active_tasks().all())

# class Pomodoro(db.Model):
#     """docstring for Pomodoro"""
#     id = db.Column(db.Integer, primary_key = True)
#     start_time = db.Column(db.DateTime)
#     end_time = db.Column(db.DateTime)
    # pomodoro = db.Column(db.Float)

#     def __init__(self, arg):
#         super(Pomodoro, self).__init__()
#         self.arg = arg
#     def 