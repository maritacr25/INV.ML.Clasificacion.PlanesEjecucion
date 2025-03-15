
#Fase Comprension de Datos - Exploracion de los datos
import pandas as pd #biblioteca para manipular datos tabulares
import matplotlib.pyplot as plt #interfaz para crear gráficos y diagramas
import Utilitarios as ut #biblioteca con utilitarios para el análisis de datos
import os #biblioteca para manipular archivos y directorios

pd.set_option('display.float_format', '{:.2f}'.format)

#cargar conjunto de datos de data/entretenimiento.csv
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'entrenamiento.csv')
conjunto_datos_planes_ejecucion = pd.read_csv(data_path, sep=';')


#limpiar datos
dataset_planes_ejecucion = ut.limpiar_datos(conjunto_datos_planes_ejecucion)
#a-Resumen estadistico de los datos
print(conjunto_datos_planes_ejecucion.describe())


#b-Analisis univariado (por cada variable categorica)
ut.analisis_univariado_barras_porcentaje(dataset_planes_ejecucion, 'Index_Suggestions_Flag')
ut.analisis_univariado_barras_porcentaje(dataset_planes_ejecucion, 'Warnings_Flag')
ut.analisis_univariado_barras_porcentaje(dataset_planes_ejecucion, 'Table_Scan_Flag')
ut.analisis_univariado_barras_porcentaje(dataset_planes_ejecucion, 'Index_Scan_Flag')  


#b.Análisis de variables continuas
# Lista de columnas de interés
nvariables_continuas = ['last_worker_time', 'last_logical_reads', 'last_elapsed_time']  
conjunto_variables_continuas = conjunto_datos_planes_ejecucion[nvariables_continuas]
print(conjunto_variables_continuas.describe())

