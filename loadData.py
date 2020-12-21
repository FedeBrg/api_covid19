import pandas as pd
from sqlalchemy import create_engine
from datetime import date

import psycopg2 as postgres
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import wget

import os


def save_data_copy():

	print("UPDATING DATA")
	filename = 'C:\\Users\\fedeb\\Desktop\\api_infovis\\Covid19Casos.csv'
	if os.path.exists(filename):
		os.remove(filename)

	url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'
	print("FETCHING DATA")
	wget.download(url)
	print("\nDATA FETCHED")
	
	
	conn = postgres.connect("dbname=api_infovis user=postgres password=postgres")

	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);


	cursor = conn.cursor()

	file = open('data_update.sql',mode='r')
 
	update_script = file.read()
 
	file.close()

	cursor.execute("DROP TABLE covid;")
	
	print("VACUUMING DB")
	os.system("vacuumdb --full api_infovis")
	print("DB VACUUMED")

	print("WRITING TO DATABASE")

	cursor.execute(update_script)

	print("UPDATE COMPLETED")

	cursor.close()
	conn.close()





