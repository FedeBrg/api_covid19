import psycopg2 as postgres
import pandas as pd
import numpy as np

pop_nacional = 45376763

poblacion = {
	2:3075646,
	6:17541141,
	10:415438,
	14:3760450,
	18:1120801,
	22:1204541,
	26:618994,
	30:1385961,
	34:605193,
	38:779212,
	42:358428,
	46:398648,
	50:2010363,
	54:1274992,
	58:664057,
	62:747610,
	66:1441988,
	70:789489,
	74:514610,
	78:374756,
	82:3563390,
	86:988245,
	90:1714487,
	94:173432

}

nombres = {
	2:"CABA",
	6:"Buenos Aires",
	10:"Catamarca",
	14:"Córdoba",
	18:"Corrientes",
	22:"Chaco",
	26:"Chubut",
	30:"Entre Ríos",
	34:"Formosa",
	38:"Jujuy",
	42:"La Pampa",
	46:"La Rioja",
	50:"Mendoza",
	54:"Misiones",
	58:"Neuquén",
	62:"Río Negro",
	66:"Salta",
	70:"San Juan",
	74:"San Luis",
	78:"Santa Cruz",
	82:"Santa Fe",
	86:"Santiago del Estero",
	90:"Tucumán",
	94:"Tierra del Fuego"

}

def last_update():
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	cursor.execute("SELECT ultima_actualizacion FROM covid LIMIT 1")

	result = cursor.fetchone()[0]

	cursor.close()
	conn.close()

	return result


def resumen_nacional():
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	cursor.execute("SELECT  count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion LIKE '%confirmado%No activo%' or clasificacion LIKE '%confirmado%No Activo%'")
	recs = cursor.fetchone()[0]

	cursor.execute("SELECT  count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado'")
	confs = cursor.fetchone()[0]


	cursor.execute('SELECT count(*) FROM covid WHERE fecha_fallecimiento IS NOT NULL')
	falls = cursor.fetchone()[0]


	cursor.execute('SELECT avg(edad) FROM covid WHERE fecha_fallecimiento IS NOT NULL')
	edad_m = cursor.fetchone()[0]


	cursor.execute("SELECT avg(edad) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado'")
	edad_c = cursor.fetchone()[0]

	result = resumen_json(recs,confs,falls,edad_m,edad_c,pop_nacional)
	cursor.close()
	conn.close()
	return result


def resumen_provincias():
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	ids = [2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94]


	pop = poblacion

	cursor.execute("SELECT  residencia_provincia_id, count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND (clasificacion LIKE '%confirmado%No activo%' or clasificacion LIKE '%confirmado%No Activo%') GROUP BY residencia_provincia_id ORDER BY residencia_provincia_id")
	recs = cursor.fetchall()

	cursor.execute("SELECT  residencia_provincia_id, count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado' GROUP BY residencia_provincia_id ORDER BY residencia_provincia_id")
	confs = cursor.fetchall()

	cursor.execute("SELECT residencia_provincia_id, count(*) FROM covid WHERE fecha_fallecimiento IS NOT NULL GROUP BY residencia_provincia_id ORDER BY residencia_provincia_id")
	falls = cursor.fetchall()

	cursor.execute("SELECT residencia_provincia_id, avg(edad) FROM covid WHERE fecha_fallecimiento IS NOT NULL GROUP BY residencia_provincia_id ORDER BY residencia_provincia_id")
	edad_m = cursor.fetchall()

	cursor.execute("SELECT residencia_provincia_id, avg(edad) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado' GROUP BY residencia_provincia_id ORDER BY residencia_provincia_id")
	edad_c = cursor.fetchall()

	response = "["

	for i in range(24):
		response += resumen_json(recs[i][1],confs[i][1],falls[i][1],edad_m[i][1],edad_c[i][1],pop[ids[i]])
		response = response[:-1]
		response += ",\"provincia\":\""+nombres[ids[i]]+"\"},"	

	
	response = response[:-1]
	response += "]"

	cursor.close()
	conn.close()

	return response



def resumen_provincia(id):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	pop = poblacion[id]

	cursor.execute(f"SELECT  count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND (clasificacion LIKE '%confirmado%No activo%' or clasificacion LIKE '%confirmado%No Activo%') AND residencia_provincia_id = {id}")
	recs = cursor.fetchone()[0]

	cursor.execute(f"SELECT  count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado' AND residencia_provincia_id = {id}")
	confs = cursor.fetchone()[0]

	cursor.execute(f"SELECT count(*) FROM covid WHERE fecha_fallecimiento IS NOT NULL AND residencia_provincia_id = {id}")
	falls = cursor.fetchone()[0]

	cursor.execute(f"SELECT avg(edad) FROM covid WHERE fecha_fallecimiento IS NOT NULL AND residencia_provincia_id = {id}")
	edad_m = cursor.fetchone()[0]

	cursor.execute(f"SELECT avg(edad) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado' AND residencia_provincia_id = {id}")
	edad_c = cursor.fetchone()[0]

	result = resumen_json(recs,confs,falls,edad_m,edad_c,pop)

	cursor.close()
	conn.close()

	return result


def resumen_departamento(id_prov,id_dep):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()


	cursor.execute(f"SELECT  count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND (clasificacion LIKE '%confirmado%No activo%' or clasificacion LIKE '%confirmado%No Activo%') AND residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep}")
	recs = cursor.fetchone()[0]

	cursor.execute(f"SELECT  count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado' AND residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep}")
	confs = cursor.fetchone()[0]

	cursor.execute(f"SELECT count(*) FROM covid WHERE fecha_fallecimiento IS NOT NULL AND residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep}")
	falls = cursor.fetchone()[0]

	cursor.execute(f"SELECT avg(edad) FROM covid WHERE fecha_fallecimiento IS NOT NULL AND residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep}")
	edad_m = cursor.fetchone()[0]

	cursor.execute(f"SELECT avg(edad) FROM covid WHERE fecha_diagnostico IS NOT NULL AND clasificacion_resumen LIKE 'Confirmado' AND residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep}")
	edad_c = cursor.fetchone()[0]

	result = resumen_json(recs,confs,falls,edad_m,edad_c)

	cursor.close()
	conn.close()

	return result


def diario_nacion(fromDate, toDate):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()
	
	where = ""

	if(fromDate != None):
		where += f" AND fecha_diagnostico >= '{fromDate}'"

	if(toDate != None):
		where += f" AND fecha_diagnostico <= '{toDate}'"


	cursor.execute('SELECT fecha_diagnostico,clasificacion_resumen, count(clasificacion_resumen) FROM covid WHERE fecha_diagnostico IS NOT NULL '+ where +' GROUP BY fecha_diagnostico,clasificacion_resumen;')


	# print('SELECT fecha_diagnostico,clasificacion_resumen, count(clasificacion_resumen) FROM covid WHERE fecha_diagnostico IS NOT NULL '+ where +' GROUP BY fecha_diagnostico,clasificacion_resumen')
	
	response = cursor.fetchall()

	cases = pd.DataFrame(response, columns =['Date', 'Type', 'Amount'])

	cases = cases.pivot_table('Amount', ['Date'], 'Type').fillna(0)




	where = ""

	if(fromDate != None):
		where += f" AND fecha_fallecimiento >= '{fromDate}'"

	if(toDate != None):
		where += f" AND fecha_fallecimiento <= '{toDate}'"

	cursor.execute('SELECT fecha_fallecimiento, count(*) FROM covid WHERE fecha_fallecimiento IS NOT NULL AND fecha_diagnostico IS NOT NULL '+where+' GROUP BY fecha_fallecimiento')
	response = cursor.fetchall()

	deaths = pd.DataFrame(response, columns =['Date', 'Fallecidos'])

	result = pd.merge(cases,deaths, on='Date', how='outer').fillna(0)

	result['Fallecidos_acum'] = result['Fallecidos'].cumsum()

	result['Confirmado_acum'] = result['Confirmado'].cumsum()
	result['Sospechoso_acum'] = result['Sospechoso'].cumsum()
	result['Descartado_acum'] = result['Descartado'].cumsum()

	cursor.close()
	conn.close()

	return result

def diario_provincia(id, fromDate, toDate):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	where = ""

	if(fromDate != None):
		where += f" AND fecha_diagnostico >= '{fromDate}'"

	if(toDate != None):
		where += f" AND fecha_diagnostico <= '{toDate}'"

	cursor.execute(f"SELECT fecha_diagnostico,clasificacion_resumen, count(clasificacion_resumen) FROM covid WHERE residencia_provincia_id = {id} AND fecha_diagnostico IS NOT NULL {where} GROUP BY fecha_diagnostico,clasificacion_resumen")

	response = cursor.fetchall()

	cases = pd.DataFrame(response, columns =['Date', 'Type', 'Amount'])

	cases = cases.pivot_table('Amount', ['Date'], 'Type').fillna(0)

	cases['Confirmado_acum'] = cases['Confirmado'].cumsum()
	cases['Sospechoso_acum'] = cases['Sospechoso'].cumsum()
	cases['Descartado_acum'] = cases['Descartado'].cumsum()

	where = ""

	if(fromDate != None):
		where += f" AND fecha_fallecimiento >= '{fromDate}'"

	if(toDate != None):
		where += f" AND fecha_fallecimiento <= '{toDate}'"

	cursor.execute(f"SELECT fecha_fallecimiento, count(*) FROM covid WHERE residencia_provincia_id = {id} AND fecha_fallecimiento IS NOT NULL {where} GROUP BY fecha_fallecimiento")

	response = cursor.fetchall()

	deaths = pd.DataFrame(response, columns =['Date', 'Fallecidos'])

	result = pd.merge(cases,deaths, on='Date', how='outer').fillna(0)

	result['Fallecidos_acum'] = result['Fallecidos'].cumsum()

	cursor.close()
	conn.close()

	return result

def diario_departamento(id_prov, id_dep, fromDate, toDate):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	where = ""

	if(fromDate != None):
		where += f" AND fecha_diagnostico >= '{fromDate}'"

	if(toDate != None):
		where += f" AND fecha_diagnostico <= '{toDate}'"

	cursor.execute(f"SELECT fecha_diagnostico,clasificacion_resumen, count(clasificacion_resumen) FROM covid WHERE residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep} AND fecha_diagnostico IS NOT NULL {where} GROUP BY fecha_diagnostico,clasificacion_resumen")

	response = cursor.fetchall()

	cases = pd.DataFrame(response, columns =['Date', 'Type', 'Amount'])

	cases = cases.pivot_table('Amount', ['Date'], 'Type').fillna(0)

	cases['Confirmado_acum'] = cases['Confirmado'].cumsum()
	cases['Sospechoso_acum'] = cases['Sospechoso'].cumsum()
	cases['Descartado_acum'] = cases['Descartado'].cumsum()

	where = ""

	if(fromDate != None):
		where += f" AND fecha_fallecimiento >= '{fromDate}'"

	if(toDate != None):
		where += f" AND fecha_fallecimiento <= '{toDate}'"

	cursor.execute(f"SELECT fecha_fallecimiento, count(*) FROM covid WHERE residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep} AND fecha_fallecimiento IS NOT NULL {where} GROUP BY fecha_fallecimiento")

	response = cursor.fetchall()

	deaths = pd.DataFrame(response, columns =['Date', 'Fallecidos'])

	result = pd.merge(cases,deaths, on='Date', how='outer').fillna(0)

	result['Fallecidos_acum'] = result['Fallecidos'].cumsum()

	cursor.close()
	conn.close()

	return result

def provincias():
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	cursor.execute("SELECT residencia_provincia_nombre, residencia_provincia_id FROM covid GROUP BY residencia_provincia_nombre, residencia_provincia_id")
	response = cursor.fetchall()

	result = pd.DataFrame(response,columns=['provincia','id'])

	result = result[result['provincia'] != 'SIN ESPECIFICAR']

	cursor.close()
	conn.close()

	return list_json(result,'provincia')

def departamentos(id):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()

	cursor.execute(f"SELECT residencia_departamento_nombre, residencia_departamento_id FROM covid WHERE residencia_provincia_id = {id} GROUP BY residencia_departamento_nombre, residencia_departamento_id")
	response = cursor.fetchall()

	result = pd.DataFrame(response,columns=['departamento','id'])

	result = result[result['departamento'] != 'SIN ESPECIFICAR']

	cursor.close()
	conn.close()

	return list_json(result,'departamento')


  # dead = 'SI' | 'NO'
  # resp = 'SI' | 'NO'
  # finc = 'Privado' | 'Público'
  # sex = 'M' | 'F'
  # ci = 'SI' | 'NO'
  # clas = 'Descartado' | 'Confirmado' | 'Sospechoso'
  # toDate, fromDate -> fechas (str)
  # toAge, fromAge -> Rango (int, -1 si no hay)
  # None para cuando no esta el parametro


def cuenta_nacional(dead, resp, finc, sex, ci, clas, fromDate, toDate, fromAge, toAge):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()


	where = where_string(dead, resp, finc, sex, ci, clas, fromDate, toDate, fromAge, toAge)

	cursor.execute("SELECT count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL"+where)

	response = cursor.fetchone()[0]

	cursor.close()
	conn.close()

	return response


def cuenta_provincia(id, dead, resp, finc, sex, ci, clas, fromDate, toDate, fromAge, toAge):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()


	where = where_string(dead, resp, finc, sex, ci, clas, fromDate, toDate, fromAge, toAge)

	cursor.execute("SELECT count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND residencia_provincia_id = "+str(id)+where)

	response = cursor.fetchone()[0]

	cursor.close()
	conn.close()

	return response

	
def cuenta_departamento(id_prov, id_dep, dead, resp, finc, sex, ci, clas, fromDate, toDate, fromAge, toAge):
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	cursor = conn.cursor()


	where = where_string(dead, resp, finc, sex, ci, clas, fromDate, toDate, fromAge, toAge)

	cursor.execute(f"SELECT count(*) FROM covid WHERE fecha_diagnostico IS NOT NULL AND residencia_provincia_id = {id_prov} AND residencia_departamento_id = {id_dep} {where}")

	response = cursor.fetchone()[0]

	cursor.close()
	conn.close()

	return response


def where_string(dead, resp, finc, sex, ci, clas, fromDate, toDate, fromAge, toAge):
	where = ""
	date = "fecha_diagnostico"
	if(dead != None):
		where += f" AND fallecido = '{dead}'"
		date = "fecha_fallecimiento"

	if(resp != None):
		where += f" AND asistencia_respiratoria_mecanica = '{resp}'"

	if(finc != None):
		where += f" AND origen_financiamiento = '{finc}'"

	if(sex != None):
		where += f" AND sexo = '{sex}'"

	if(ci != None):
		where += f" AND cuidado_intensivo = '{ci}'"

	if(clas != None):
		where += f" AND clasificacion_resumen = '{clas}'"

	if(fromDate != None):
		where += f" AND {date} >= '{fromDate}'"

	if(toDate != None):
		where += f" AND {date} <= '{toDate}'"

	if(fromAge != None):
		where += f" AND edad >= {fromAge}"

	if(toAge != None):
		where += f" AND edad <= {toAge}"

	return where


def resumen_json(recs, confs, falls, edad_m, edad_c, pop=-1):
	result = "{ "
	result += "\"recuperados\": "+str(recs) + ","
	result += "\"casos\":"+str(confs)+ ","
	result += "\"fallecidos\": "+str(falls)+ ","
	if(pop > 0):
		result += "\"poblacion\": "+str(pop)+ ","
		result += "\"casos_por_millon\": "+str(np.floor(1000000*confs/pop))+ ","
		result += "\"fallecidos_por_millon\": "+str(np.floor(1000000*falls/pop))+ ","
		result += "\"recuperados_por_millon\": "+str(np.floor(1000000*recs/pop))+ ","


	result += "\"tasa_recuperados\": "+str("%.4f" % (1 - falls/confs)) + ","
	result += "\"edad_media_fallecidos\": "+str(np.floor(edad_m)) + ","
	result += "\"edad_media_contagios\": "+str(np.floor(edad_c))
	result += " }"

	return result


def list_json(data,region):
	result = "["

	for index, row in data.iterrows():
		result += "{\"id\":"+str(row['id'])+",\""+region+"\":\""+row[region]+"\"},"

	result = result[:-1]

	result += "]"
	
	return result