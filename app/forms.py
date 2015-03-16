from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class TaskForm(Form):
    task = StringField('task', validators=[DataRequired()])
