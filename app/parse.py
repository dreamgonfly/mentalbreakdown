from dateutil.parser import parse
from datetime import datetime, timedelta
import re

def parse_todo(raw):
	parsed = {}
	time_format = '(\d+-)?\d+-\d+ \d+:\d+(:\d+)?|(\d+-)?\d+-\d+|\d+:\d+(:\d+)?|\d+h|\d+d|\d+m'
	matched = re.match(r'(?P<todo>.*?)( \((?P<required_time>\d+)\)| (?P<scheduled>{0})?~(?P<due>{0})?)* ?$'.format(time_format), raw)
	parsed['todo'] = matched.group('todo')
	if matched.group('required_time'):
		parsed['required_time'] = int(matched.group('required_time'))
	if matched.group('scheduled'):
		scheduled_raw = matched.group('scheduled')
		if scheduled_raw[-1] == 'd':
			day = int(scheduled_raw[:-1])
			scheduled = datetime.now() + timedelta(day)
			scheduled = datetime(scheduled.year, scheduled.month, scheduled.day, 0, 0)
		elif scheduled_raw[-1] == 'h':
			hour = int(scheduled_raw[:-1])
			scheduled = datetime.now() + timedelta(hours = hour)
		elif scheduled_raw[-1] == 'm':
			minute = int(scheduled_raw[:-1])
			scheduled = datetime.now() + timedelta(minutes = minute)
		else:
			scheduled = parse(scheduled_raw)
		parsed['scheduled'] = scheduled
	if matched.group('due'):
		due_raw = matched.group('due')
		if due_raw[-1] == 'd':
			day = int(due_raw[:-1])
			due = datetime.now() + timedelta(day)
			due = datetime(due.year, due.month, due.day, 23, 59)
		elif due_raw[-1] == 'h':
			hour = int(due_raw[:-1])
			due = datetime.now() + timedelta(hours = hour)
		elif due_raw[-1] == 'm':
			minute = int(due_raw[:-1])
			due = datetime.now() + timedelta(minutes = minute)
		else:
			due = parse(due_raw)
			if due.hour == 0 and due.minute == 0:
				due = due + timedelta(1) - timedelta(minutes = 1)
		parsed['due'] = due
	return parsed
