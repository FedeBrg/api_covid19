# API Covid-19

## Introducción
Esta API fue desarrollada como evaluacion final para la materia `72.74 - Visualización de la Información`. La misma fue desarrollada en lenguaje Python utilizando `Flask` para poder hacer los pedidos de información.

## Autores
Bergagna, Federico Manuel. Baader, Juan Martín. Rodríguez Brizi, Manuel

## Instrucciones

Son necesarias un par de librerias, para la instalación de las mismas se puede utilizar pip install a medida que sean requeridas.

Con las librerias instaladas, es necesario contar con un Postgres instalado en la computadora, con una base de datos llamada `api_infovis`. Se asume que el usuario es **postgres** y la contraseña es **postgres**. 

Ahora estamos en condiciones de correr la API, a través del comando:

	$> python api.py update

La misma descargará el archivo CSV (tanto por primera vez o para actualizar el archivo que ya esté descargado) desde el Ministerio de Salud de la Nación y se encargará de popular la base de datos.

Por defecto, la API corre en `localhost:5000`. Se le pueden realizar consultas, por ejemplo, a través de cURL.

En el caso de que no querramos actualizar el archivo del Ministerio de Salud y solamente querramos correr la API con el archivo que ya tenemos, corremos:

	$> python api.py

Pero debemos haber corrido al menos una vez el primer comando para popular la base de datos.

## Comandos
En los siguientes ejemplos se utilizará cURL para hacer las llamadas a la API.

1) Última actualización del archivo:
	
		$> curl localhost:5000/last_update


2) Resumen nacional:

		$> curl localhost:5000/nacion/resumen
		
		
3) Resumen de todas las provincias:
	
		$> curl localhost:5000/nacion/provincias/resumen


4)  Resumen de una provincia determinada:

		$> curl localhost:5000/nacion/provincias/{id}/resumen

5) Resúmen de un departamento/partido en una provincia:

		$> curl localhost:5000/nacion/provincias/{id_prov}/departamentos/{id_dep}/resumen
		
	
	Donde **id_prov** es el id de provincia y **id_dep** es el id del departamento/partido.
	
	Los posibles valores de **id_prov** se obtienen mediante:
	
			$> curl localhost:5000/nacion/provincias
			
	Los posibles valores de **id_dep** se obtienen mediante:
	
			$> curl localhost:5000/nacion/provincias/{id_prov}/departamentos


6) Casos diarios en Nación:

		$> curl localhost:5000/nacion/diario

7) Casos diarios en una provincia:

		$> curl localhost:5000/nacion/provincias/{id}/diario

	Donde **id** es el id de la provincia.

8) Casos diarios en un departamento/partido:

		$> curl localhost:5000/nacion/provincias/{id_prov}/departamentos/{id_dep}/diario

	Donde **id_prov** es el id de la provincia y **id_dep** es el id del departamento/partido.

9) Nombres y id's de las provincias:

		$> curl localhost:5000/nacion/provincias

10) Nombres de los departamentos/partidos de una provincia:

		$> curl localhost:5000/nacion/provincias/{id}/departamentos

	Donde **id** es el id de la provincia.

11) Cantidad de casos a nivel nacional donde se cumplen condiciones determinadas según los Query Parameters provistos. Los mismos pueden ser:

	a) fallecidos = 'SI' | 'NO' . Contar fallecidos (por defecto es diagnosticados) 
	
	b) respirador = 'SI' | 'NO' . Se precisó de respirador  
	
	c) financiamiento = 'Privado' | 'Público' . Tipo de financiamiento  
	
	d) sexo = 'F' | 'M' . Sexo de la persona 
	
	e) intensivo = 'SI' | 'NO' . Es un paciente en terapia intensiva 
	
	f) tipo = 'Descartado' | 'Confirmado' | 'Sospechoso' . Clasificación 
	
	g) fechaD = Fecha de inicio para contar
	
	h) fechaH = Fecha de fin para contar 
	
	i) edadD = Inicio de edad de los pacientes
	
	j) edadH = Final de edad de los pacientes
	

Un ejemplo para tener la cuenta de casos entre los días 2 y 5 de diciembre:

		$> http://localhost:5000/nacion/cuenta?fechaD=2-12-2020&fechaH=5-12-2020

12)  De forma similar al caso anterior puede hacerse para una provincia particular con:

	$> curl localhost:5000/nacion/provincias/{id}/cuenta

13) De forma similar a los casos anteriores puede hacerse para un departamento/partido:

		$> curl localhost:5000/nacion/provincias/{id_prov}/departamentos/{id_dep}/cuenta
