#Análisis de componentes principales
import pandas as pd
import Utilitarios as ut #biblioteca con utilitarios para el análisis de datos
import os #biblioteca para manipular archivos y directorios

#cargar conjunto de datos de data/entretenimiento.csv
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'entrenamiento.csv')
conjunto_datos_planes_ejecucion = pd.read_csv(data_path, sep=';')


nvariables = [ 'Categoria','last_elapsed_time','last_logical_reads','Index_Suggestions_Flag', 'Warnings_Flag','Table_Scan_Flag','Index_Scan_Flag','last_worker_time','last_logical_reads']  
subconjuntovariables = conjunto_datos_planes_ejecucion[nvariables]

# Calcula la matriz de covarianza
matriz_covarianza = subconjuntovariables.cov()

# Muestra la matriz de covarianza
#print(matriz_covarianza)


ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'last_logical_reads', 'Categoria')
ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'Index_Suggestions_Flag', 'Categoria')
ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'Warnings_Flag', 'Categoria')
ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'Table_Scan_Flag', 'Categoria')
ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'Index_Scan_Flag', 'Categoria')
ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'last_worker_time', 'Categoria')
ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'last_logical_reads', 'Categoria')
ut.examinar_varianza_pca(conjunto_datos_planes_ejecucion, 'last_elapsed_time', 'Categoria')

