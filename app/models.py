from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    raw = db.Column(db.String(140))
    todo = db.Column(db.String(100))
    estimated_time = db.Column(db.Integer)
    due = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return '<Task {}>'.format(self.raw)

    @staticmethod
    def active_tasks():
    	return Task.query.filter_by(completed = False)

    @staticmethod
    def pick_one():
    	return Task.active_tasks().order_by(Task.estimated_time)