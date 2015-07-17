from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app, db
import csv
from os import path
import logging

PERIODIC_TABLE = path.join(path.dirname(__file__), 'periodic_table.csv')
LOG_FILE = path.join(path.dirname(__file__), 'mass_calculator.log')

logger = logging.getLogger('mass calculator logger')
formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

@app.route('/mass_calculator')
def mass_calculator():
	return render_template('mass_calculator.html')

@app.route('/calculate_mass', methods=['POST'])
def calculate_mass():
	# request.form.getlist('elements[]')
	data = request.get_json(force=True)
	logger.info("mass_calculator_input - " + str(data))

	def molar_mass(element):
		with open( PERIODIC_TABLE ) as table:
		    for row in csv.reader(table):
		        if row[1] == ' ' + element + ' ':
		        	return float(row[3].strip().split('(')[0])

	formula = {element:ratio for element, ratio in zip(data['elements'], data['ratios']) if element != '' and ratio != ''}
	result = {}
	for element in formula:
		reference_atoms = float(data['reference_mass']) / molar_mass(data['reference_element']) / float(formula[data['reference_element']])
		result[element] =  reference_atoms * float(formula[element]) * molar_mass(element)
	
	logger.info("mass_calculator_output - " + str(result))
	return jsonify(result)

