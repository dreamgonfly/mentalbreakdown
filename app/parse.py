from dateutil.parser import parse
from datetime import datetime, timedelta
import re

def parse_todo(raw):
	parsed = {}
	matched = re.match(r'(.*?)( ~.*| \(\d+\))*$', raw)
	parsed['todo'] = matched.groups()[0]
	estimated_time_raw = re.search(r' \((\d+)\)', raw)
	if estimated_time_raw:
		parsed['estimated_time'] = int(estimated_time_raw.groups()[0])
	due_raw = re.search(r' ~((\d+-)?\d+-\d+ \d+:\d+(:\d+)?|(\d+-)?\d+-\d+|\d+:\d+(:\d+)?|\d+h|\d+d|\d+m)', raw)
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
