import flask
from queryData import *
from flask import request, jsonify

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from loadData import *

import sys

import json




def api_save_data():
	save_data_copy()

scheduler = BackgroundScheduler(daemon = True)
scheduler.add_job(func=api_save_data, trigger="interval", hours=24)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app = flask.Flask(__name__)

pool = None

@app.route('/last_update', methods=['GET'])
def api_last_update():
	result = last_update()
	return result


@app.route('/nacion/provincias/resumen', methods=['GET'])
def api_resumen_provincias():
	return (resumen_provincias())


@app.route('/nacion/resumen', methods=['GET'])
def api_resumen_nacion():
	return json.loads(resumen_nacional())


@app.route('/nacion/provincias/<int:id>/resumen', methods=['GET'])
def api_resumen_provincia(id):
    return json.loads(resumen_provincia(id))


@app.route('/nacion/provincias/<int:id_prov>/departamentos/<int:id_dep>/resumen', methods=['GET'])
def api_resumen_departamento(id_prov, id_dep):
    return json.loads(resumen_departamento(id_prov, id_dep))


@app.route('/nacion/diario', methods=['GET'])
def api_diario_nacion():
	queryParams = request.args

	fechaD = queryParams.get('fechaD')
	fechaH = queryParams.get('fechaH')

	return diario_nacion(fechaD, fechaH).reset_index(drop=True).to_json(orient='records')


@app.route('/nacion/provincias/<int:id>/diario', methods=['GET'])
def api_diario_provinica(id):
	queryParams = request.args

	fechaD = queryParams.get('fechaD')
	fechaH = queryParams.get('fechaH')
	return diario_provincia(id,fechaD, fechaH).reset_index(drop=True).to_json(orient='records')

@app.route('/nacion/provincias/<int:id_prov>/departamentos/<int:id_dep>/diario', methods=['GET'])
def api_diario_departamento(id_prov, id_dep):
	queryParams = request.args

	fechaD = queryParams.get('fechaD')
	fechaH = queryParams.get('fechaH')
	return diario_departamento(id_prov, id_dep,fechaD, fechaH).reset_index(drop=True).to_json(orient='records')


@app.route('/nacion/provincias', methods=['GET'])
def api_provincias():
    return (provincias())


@app.route('/nacion/provincias/<int:id>/departamentos', methods=['GET'])
def api_departamentos(id):
    return departamentos(id)


@app.route('/nacion/cuenta', methods=['GET'])
def api_cuenta_nacion():
	queryParams = request.args

	fallecidos = queryParams.get('fallecidos')
	respirador = queryParams.get('respirador')
	financiamiento = queryParams.get('financiamiento')
	sexo = queryParams.get('sexo')
	intensivo = queryParams.get('intensivo')
	tipo = queryParams.get('tipo')
	fechaD = queryParams.get('fechaD')
	fechaH = queryParams.get('fechaH')
	edadD = queryParams.get('edadD')
	edadH = queryParams.get('edadH')

	return str(cuenta_nacional(fallecidos, respirador, financiamiento, sexo, intensivo, tipo, fechaD, fechaH, edadD, edadH))


@app.route('/nacion/provincias/<int:id>/cuenta', methods=['GET'])
def api_cuenta_provincia(id):
	queryParams = request.args

	fallecidos = queryParams.get('fallecidos')
	respirador = queryParams.get('respirador')
	financiamiento = queryParams.get('financiamiento')
	sexo = queryParams.get('sexo')
	intensivo = queryParams.get('intensivo')
	tipo = queryParams.get('tipo')
	fechaD = queryParams.get('fechaD')
	fechaH = queryParams.get('fechaH')
	edadD = queryParams.get('edadD')
	edadH = queryParams.get('edadH')

	return str(cuenta_provincia(id,fallecidos, respirador, financiamiento, sexo, intensivo, tipo, fechaD, fechaH, edadD, edadH))


@app.route('/nacion/provincias/<int:id_prov>/departamentos/<int:id_dep>/cuenta', methods=['GET'])
def api_cuenta_departamento(id_prov,id_dep):
	queryParams = request.args

	fallecidos = queryParams.get('fallecidos')
	respirador = queryParams.get('respirador')
	financiamiento = queryParams.get('financiamiento')
	sexo = queryParams.get('sexo')
	intensivo = queryParams.get('intensivo')
	tipo = queryParams.get('tipo')
	fechaD = queryParams.get('fechaD')
	fechaH = queryParams.get('fechaH')
	edadD = queryParams.get('edadD')
	edadH = queryParams.get('edadH')

	return str(cuenta_departamento(id_prov,id_dep,fallecidos, respirador, financiamiento, sexo, intensivo, tipo, fechaD, fechaH, edadD, edadH))




if(len(sys.argv)>1):
	if(sys.argv[1] == 'update'):
		api_save_data()

app.run()
