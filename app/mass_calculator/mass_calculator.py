from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app, db
import csv

PERIODIC_TABLE = 'periodic_table.csv'

@app.route('/mass_calculator')
def mass_calculator():
	return render_template('mass_calculator.html')

@app.route('/calculate_mass', methods=['POST'])
def calculate_mass():
	# request.form.getlist('elements[]')
	data = request.get_json(force=True)

	def molar_mass(element):
		with open(PERIODIC_TABLE) as table:
		    for row in csv.reader(table):
		        if row[1] == ' ' + element + ' ':
		        	return float(row[3].strip().split('(')[0])

	formula = {element:ratio for element, ratio in zip(data['elements'], data['ratios']) if element != '' and ratio != ''}
	result = {}
	for element in formula:
		reference_atoms = float(data['reference_mass']) / molar_mass(data['reference_element']) / float(formula[data['reference_element']])
		result[element] =  reference_atoms * float(formula[element]) * molar_mass(element)

	return jsonify(result)

