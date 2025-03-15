import pandas as pd
import matplotlib.pyplot as plt #interfaz para crear gráficos y diagramas
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
import numpy as np

def agregar_columnas_fecha(dataset, columna_fecha):
    dataset[columna_fecha] = pd.to_datetime(dataset[columna_fecha])
    dataset['Year'] = dataset[columna_fecha].dt.year
    dataset['Month'] = dataset[columna_fecha].dt.month
    dataset['Day'] = dataset[columna_fecha].dt.day
    dataset['Hour'] = dataset[columna_fecha].dt.hour
    dataset['Minute'] = dataset[columna_fecha].dt.minute
    dataset['Second'] = dataset[columna_fecha].dt.second
    return dataset

def limpiar_datos(dataset):
    dataset = dataset.dropna()
    dataset = dataset.drop_duplicates()
    return dataset

def analisis_univariado_barras(dataset, columna):
    valores = dataset[columna].value_counts().sort_index()
    valores.plot(kind='bar')
    plt.title('Análisis Univariado de ' + columna)
    plt.grid(True)
    plt.show()
    return valores
    
def analisis_univariado_barras_porcentaje(dataset, columna):
    valores = dataset[columna].value_counts().sort_index()
    total = valores.sum()
    porcentajes = (valores / total) * 100
    
    ax = valores.plot(kind='bar')
    plt.title('Análisis Univariado de ' + columna)
    plt.grid(True)
    
    # Añadir etiquetas de porcentaje encima de las barras
    for i in ax.containers:
        ax.bar_label(i, labels=[f'{v} ({p:.2f}%)' for v, p in zip(valores, porcentajes)], label_type='edge')
    
    plt.show()
    return valores
   
def examinar_varianza_pca(conjunto,columna_1, columna_2):
    nvariables = [columna_1,columna_2]
    conjunto_variables = conjunto[nvariables]
    #print(conjunto_variables.describe())
    # Estandarización de los datos
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(conjunto_variables)
    #Aplicar PCA
    pca_conjunto = PCA(n_components=2)  # Elegir el número de componentes principales
    principal_components = pca_conjunto.fit_transform(data_scaled)
    explained_variance = pca_conjunto.explained_variance_ratio_
    print("Varianza explicada para " + columna_1 + " respecto a "+ columna_2+":", explained_variance)
    return explained_variance

# comentar todas las lineas siguientes
# def graficar_varianza_pca(principal_components,columna_1, columna_2):
#     # Graficar los componentes principales
#     plt.figure(figsize=(8,6))
#     plt.scatter(principal_components[:, 0], principal_components[:, 1])
#     plt.xlabel(columna_1)
#     plt.ylabel(columna_2)
#     plt.title('PCA: Componentes: ' + columna_1 + ' y ' + columna_2)
#     plt.grid()
#     plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.api as sm


def probar_normalidad_visual(datos, columna):
    datos_columna = datos[columna]
    
    # Histograma
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(datos_columna, kde=True)
    plt.title('Histograma de ' + columna)
    
    # Gráfico Q-Q
    plt.subplot(1, 2, 2)
    sm.qqplot(datos_columna, line='s')
    plt.title('Gráfico Q-Q de ' + columna)
    
    plt.tight_layout()
    plt.show()


def PNE_Shapiro(datos, columna):
    datos = datos[columna]  
    stat, p = stats.shapiro(datos)
    print(' Shapiro: stat=%.3f, p=%.3f' % (stat, p))

def PNE_KolmogorovSmirnov(datos, columna):
    datos = datos[columna]  
    stat, p = stats.kstest(datos, 'norm')
    print(' Kolmogorov-Smirnov: stat=%.3f, p=%.3f' % (stat, p))

def Pne_Anderson(datos, columna):
    datos = datos[columna]  
    result = stats.anderson(datos)
    print(' Anderson: stat=%.3f' % (result.statistic))
    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < result.critical_values[i]:
            print(columna + ' Anderson: %.3f: %.3f, datos parecen normales (no se rechaza H0)' % (sl, cv))

def PNE_Analitico(datos, columna):
    print('Pruebas de normalidad para ' + columna)
    PNE_Shapiro(datos, columna)
    PNE_KolmogorovSmirnov(datos, columna)
    Pne_Anderson(datos, columna)
    print('\n')

def probar_normalidad_estadistica(datos, columna):
    datos = datos[columna]
    stat, p = stats.shapiro(datos)
    print(columna + ' stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
        print(columna +': No se rechaza la hipótesis nula: los datos parecen normales')
    else:
        print(columna +': Se rechaza la hipótesis nula: los datos no parecen normales')
    return p

def probar_normalidad_estadistica_transformacion_logaritmica(datos, columna):
    datos = datos[columna]
     # Transformación logarítmica
    datos = np.log(datos + 1)
    stat, p = stats.shapiro(datos)
    print(columna + ' stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.06:
        print(columna +': No se rechaza la hipótesis nula: los datos parecen normales')
    else:
        print(columna +': Se rechaza la hipótesis nula: los datos no parecen normales')
    return p

def graficar_histograma_curva_distribucion_normal(conjunto,columna):
    datos = conjunto[columna]
    # Parámetros de la distribución normal
    media = datos.mean()
    desviacion_estandar = datos.std()


    # Crear el histograma de los datos
    plt.hist(datos, bins=30, density=True, alpha=0.6, color='g')

    # Crear una curva de distribución normal
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = np.exp(-0.5*((x - media)/desviacion_estandar)**2) / (desviacion_estandar * np.sqrt(2 * np.pi))
    plt.plot(x, p, 'k', linewidth=2)
    title = "Histograma y curva de distribución normal " + columna
    plt.title(title)
    plt.xlabel('Valores')
    plt.ylabel('Densidad')
    plt.show()

def graficar_histograma_transformacion_logaritmica(conjunto,columna):
    datos = conjunto[columna]
    # Transformación logarítmica
    datos = np.log(datos + 1)
    # Crear el histograma de los datos
    plt.hist(datos, bins=30, density=True, alpha=0.6, color='g')
    # Crear una curva de distribución normal
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = np.exp(-0.5*((x - datos.mean())/datos.std())**2) / (datos.std() * np.sqrt(2 * np.pi))
    plt.plot(x, p, 'k', linewidth=2)
    title = "Histograma y curva de distribución normal " + columna
    plt.title(title)
    plt.xlabel('Valores')
    plt.ylabel('Densidad')
    plt.show()