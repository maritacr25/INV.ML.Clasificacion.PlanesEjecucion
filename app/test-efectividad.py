import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
import os #biblioteca para manipular archivos y directorios

#cargar conjunto de datos de data/entretenimiento.csv
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'entrenamiento.csv')
df = pd.read_csv(data_path, sep=';')

# Seleccionar las variables continuas y la variable objetivo
nvariables_continuas = ['last_elapsed_time', 'last_logical_reads', 'Index_Suggestions_Flag', 'Warnings_Flag', 'Index_Scan_Flag', 'last_worker_time', 'last_logical_reads']
subconjuntovariables = pd.DataFrame(df, columns=nvariables_continuas)
y = df['Categoria'].map({1: 0, 2: 1})  # Map values to {0, 1}
X = subconjuntovariables

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Crear una lista de modelos supervisados
modelos = {
    'Decision Tree': DecisionTreeClassifier(),
    'Logistic Regression': LogisticRegression(max_iter=200, random_state=42),
    'SVM': SVC(probability=True, random_state=42),
    'k Neighbors': KNeighborsClassifier(n_neighbors=5),
    'Naives Bayes': GaussianNB(),
    'Red Neuronal': MLPClassifier(hidden_layer_sizes=(10, 10, 10, 10, 10, 10, 10), max_iter=1000, random_state=42),
    'Rain Forest' :  RandomForestClassifier(n_estimators=500, random_state=42)
}

# Entrenar y evaluar cada modelo
resultados = {}
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    precision = accuracy_score(y_test, y_pred)
    resultados[nombre] = precision


# Comparar las precisiones
print('Comparación de precisiones:')
print('--------------------------')
for nombre, precision in resultados.items():
    print(f'{nombre}: {precision*100:.2f}%')
print('--------------------------')
print('Mejor modelo:', max(resultados, key=resultados.get))
