from dateutil.parser import parse
from datetime import datetime, timedelta
import re

def parse_todo(raw):
	parsed = {}
	time_format = '((\d+-)?\d+-\d+ \d+:\d+(:\d+)?|(\d+-)?\d+-\d+|\d+:\d+(:\d+)?|\d+h|\d+d|\d+m)'
	matched = re.match(r'(.*?)( \(\d+\)| {0}~{0}| {0}~| ~{0})* ?$'.format(time_format), raw)
	parsed['todo'] = matched.groups()[0]
	required_time_raw = re.search(r' \((\d+)\)', raw)
	if required_time_raw:
		parsed['required_time'] = int(required_time_raw.groups()[0])
	scheduled_raw = re.search(r' {}~'.format(time_format), raw)
	if scheduled_raw:
		scheduled_raw = scheduled_raw.groups()[0]
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
			if scheduled.hour == 0 and scheduled.minute == 0:
				scheduled = scheduled + timedelta(1) - timedelta(minutes = 1)
		parsed['scheduled'] = scheduled
	due_raw = re.search(r' [^~]+~{}'.format(time_format), raw)
	if due_raw:
		due_raw = due_raw.groups()[0]
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
