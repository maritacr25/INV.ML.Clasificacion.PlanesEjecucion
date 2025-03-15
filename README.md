# Proyecto de Clasificación y Análisis Estadístico

Este proyecto es una investigacion que explora si con modelos de clasificación de Machine Learning es posible determinar si consultas SQL que requieren ser optimizadas, pueden ser identificadas utilizando información estadística y planes de ejecución del motor de base de datos SQL Server.

Contiene varios scripts de Python para realizar análisis estadísticos y de clasificación en conjuntos de datos. A continuación se describen los archivos y sus funcionalidades principales.

## Estructura del Proyecto

```
main.py
__pycache__/
    Utilitarios.cpython-312.pyc
app/
    analisiseda.py
    curvaroc.py
    marboldecision.py
    mknearestneighbors.py
    mnaivebayes.py
    mramdomforest.py
    mredesneuronales.py
    normalidad-estadistica.py
    pca.py
    regresionlogistica.py
    test-efectividad.py
    Utilitarios.py
    __pycache__/
        analisiseda.cpython-312.pyc
        Utilitarios.cpython-312.pyc
data/
    entrenamiento.csv
script/
    estructura.sql
```

## Archivos Principales

### `main.py`
Archivo principal para ejecutar el proyecto.

### Carpeta `app/`
Contiene los scripts para diferentes análisis y modelos de clasificación:

- `analisiseda.py`: Análisis exploratorio de datos.
- `curvaroc.py`: Generación de curvas ROC para todos los modelos de clasificación estudiados en este proyecto.
- `marboldecision.py`: Implementación del modelo árboles de decisión.
- `mknearestneighbors.py`: Implementación de K-Nearest Neighbors.
- `mnaivebayes.py`: Implementación de Naive Bayes.
- `mramdomforest.py`: Implementación de Random Forest.
- `mredesneuronales.py`: Implementación de redes neuronales.
- `normalidad-estadistica.py`: Pruebas de normalidad estadística.
- `pca.py`: Análisis de Componentes Principales (PCA).
- `regresionlogistica.py`: Implementación de regresión logística.
- `test-efectividad.py`: Pruebas de efectividad de los modelos.
- `Utilitarios.py`: Funciones utilitarias para el análisis de datos.

### Carpeta `data/`
Contiene los conjuntos de datos utilizados en el proyecto:

- `entrenamiento.csv`: Conjunto de datos de entrenamiento ejemplo con información relacionada a estadísiticas de planes de ejecución SQL.

### Carpeta `script/`
Contiene un script sql con las tablas y procedimientos almacenados requeridos para la captura de los datos.

-  `estructura.sql` : crea tablas: DSBase y QueryStats, además de los procedimientos almacenados: InsertQueryStats y InsertDataSetBase. También se define los jobs que capturan los datos.

## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    ```
2. Navega al directorio del proyecto:
    ```sh
    cd <NOMBRE_DEL_PROYECTO>
    ```
3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar el proyecto, simplemente ejecuta el archivo de la opcion que deseas analizar, por ejemplo `analisiseda.py`:
```sh
cd .\app\
python analisiseda.py
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.