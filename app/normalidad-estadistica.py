#Prueba Normalidad Estadistica
import scipy.stats as stats
import pandas as pd
import Utilitarios as ut
import os #biblioteca para manipular archivos y directorios

#cargar conjunto de datos de data/entretenimiento.csv
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'entrenamiento.csv')
datos = pd.read_csv(data_path, sep=';')

pd.set_option('display.float_format', '{:.2f}'.format)
datos = ut.limpiar_datos(datos)
#print(datos.describe())

ut.PNE_Analitico(datos, 'last_worker_time')
ut.PNE_Analitico(datos, 'last_logical_reads')
ut.PNE_Analitico(datos, 'last_elapsed_time')
ut.PNE_Analitico(datos, 'Index_Suggestions_Flag')
ut.PNE_Analitico(datos, 'Warnings_Flag')
ut.PNE_Analitico(datos, 'Index_Scan_Flag')

ut.graficar_histograma_curva_distribucion_normal(datos,'last_worker_time')
ut.graficar_histograma_curva_distribucion_normal(datos,'last_logical_reads')    
ut.graficar_histograma_curva_distribucion_normal(datos,'last_elapsed_time')
ut.graficar_histograma_curva_distribucion_normal(datos,'Index_Suggestions_Flag')
ut.graficar_histograma_curva_distribucion_normal(datos,'Warnings_Flag')
ut.graficar_histograma_curva_distribucion_normal(datos,'Index_Scan_Flag')


#ut.probar_normalidad_estadistica(datos,'last_worker_time')
#ut.probar_normalidad_visual(datos,'last_worker_time')
#ut.probar_normalidad_estadistica(datos,'last_logical_reads')
#ut.probar_normalidad_estadistica(datos,'last_elapsed_time') 
#ut.probar_normalidad_estadistica(datos,'Index_Suggestions_Flag')
#ut.probar_normalidad_estadistica(datos,'Warnings_Flag')
#ut.probar_normalidad_estadistica(datos,'Table_Scan_Flag')
#ut.probar_normalidad_estadistica(datos,'Index_Scan_Flag')   


#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'last_worker_time')
#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'last_worker_time')
#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'last_logical_reads')
#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'last_elapsed_time') 
#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'Index_Suggestions_Flag')
#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'Warnings_Flag')
#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'Table_Scan_Flag')
#ut.probar_normalidad_estadistica_transformacion_logaritmica(datos,'Index_Scan_Flag')   

#ut.graficar_histograma_transformacion_logaritmica(datos,'last_worker_time')
#ut.graficar_histograma_transformacion_logaritmica(datos,'last_logical_reads')    


