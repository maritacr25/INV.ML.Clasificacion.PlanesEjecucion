import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, accuracy_score
import matplotlib.pyplot as plt

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
    'Rain Forest': RandomForestClassifier(n_estimators=500, random_state=42)
}

# Entrenar y evaluar cada modelo
resultados = {}
plt.figure(figsize=(10, 8))

for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    precision = accuracy_score(y_test, y_pred)
    resultados[nombre] = precision
    
    # Calcular las probabilidades de predicción
    if hasattr(modelo, "predict_proba"):
        y_scores = modelo.predict_proba(X_test)[:, 1]
    else:  # SVM
        y_scores = modelo.decision_function(X_test)
    
    # Calcular la curva ROC y el AUC
    fpr, tpr, _ = roc_curve(y_test, y_scores)
    roc_auc = auc(fpr, tpr)
    
    # Graficar la curva ROC
    plt.plot(fpr, tpr, lw=2, label=f'{nombre} (área = {roc_auc:.2f})')

# Graficar la línea de referencia
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')

# Configurar la gráfica
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tasa de Falsos Positivos')
plt.ylabel('Tasa de Verdaderos Positivos')
plt.title('Curvas ROC para diferentes modelos')
plt.legend(loc="lower right")
plt.show()

# Comparar las precisiones
print('Comparación de precisiones:')
for nombre, precision in resultados.items():
    print(f'{nombre}: {precision*100:.2f}%')