from datetime import datetime, timedelta
from random import random
from config import LAMBDA, REFRESH_TIME

def prioritize(tasks):
	for task in tasks:
		task.priority = 0

		task.priority += 1 / (task.estimated_time + 1)

		if task.due:		
			time_remaining = task.due - datetime.now()
			if task.estimated_time * 5 > time_remaining:
				task.priority += 1
			else:
				task.priority += (task.estimated_time * 5) / time_remaining

		#randomize
		task.priority += random()/100

		if datetime.now() - task.last_notnow < REFRESH_TIME:
			task.priority *= LAMBDA ** task.number_of_notnow

	return tasks

def pick_one(tasks):
	if not tasks:
		return None
	prioritized = prioritize(tasks)
	ordered = sorted(prioritized, key = lambda p: p.priority, reverse = True)
	return ordered[0]
