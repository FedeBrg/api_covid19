
CREATE TABLE covid (
   id_evento_caso INT PRIMARY KEY,
   sexo VARCHAR(2),
   edad INT,
   edad_años_meses VARCHAR ( 15 ),
   residencia_pais_nombre text,
   residencia_provincia_nombre VARCHAR ( 30 ),
   residencia_departamento_nombre VARCHAR ( 30 ),
   carga_provincia_nombre text,
   fecha_inicio_sintomas text,
   fecha_apertura text,
   sepi_apertura text,
   fecha_internacion text,
   cuidado_intensivo VARCHAR ( 2 ),
   fecha_cui_intensivo text,
   fallecido VARCHAR ( 2 ),
   fecha_fallecimiento DATE,
   asistencia_respiratoria_mecanica VARCHAR ( 2 ),
   carga_provincia_id text,
   origen_financiamiento VARCHAR ( 15 ),
   clasificacion VARCHAR,
   clasificacion_resumen VARCHAR,
   residencia_provincia_id INT,
   fecha_diagnostico DATE,
   residencia_departamento_id INT,
   ultima_actualizacion text
);

COPY covid FROM 'C:\Users\fedeb\Desktop\api_infovis\Covid19Casos.csv' CSV HEADER;

DELETE FROM covid WHERE fecha_diagnostico < '2019-12-31';

UPDATE covid SET edad = 1 WHERE edad_años_meses LIKE 'Meses';
