import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import os #biblioteca para manipular archivos y directorios

#cargar conjunto de datos de data/entretenimiento.csv
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'entrenamiento.csv')
df = pd.read_csv(data_path, sep=';')


nvariables_continuas = [ 'last_elapsed_time','last_logical_reads','Index_Suggestions_Flag', 'Warnings_Flag','Index_Scan_Flag','last_worker_time','last_logical_reads']  
subconjuntovariables = pd.DataFrame(df, columns=nvariables_continuas)
y = df['Categoria'] 
X = subconjuntovariables
y_binary = np.where(y == 2, 1,0)

categories_names = ['POR OPTIMIZAR','OPTIMIZADO']
categories =y

print(categories_names)
print(categories)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.3, random_state=42)


# Crear el clasificador de árbol de decisión
clf = DecisionTreeClassifier()

# Ajustar el modelo con los datos de entrenamiento
clf.fit(X_train, y_train)

# Realizar predicciones con el conjunto de prueba
y_pred = clf.predict(X_test)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión: {accuracy*100:.2f}')

# Imprimir el reporte de clasificación
print('Reporte de clasificación:')
print(classification_report(y_test, y_pred))

# Imprimir la matriz de confusión
print('Matriz de confusión:')
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Visualizar la matriz de confusión usando seaborn
plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=categories_names, yticklabels=categories_names)
plt.xlabel('Predicción')
plt.ylabel('Actual')
plt.title('Matriz de Confusión')
plt.show()

from sklearn.tree import plot_tree

plt.figure(figsize=(20,10))
plot_tree(clf, filled=True, feature_names=nvariables_continuas, class_names=categories_names, fontsize=10)
plt.show()

############### Calcular Curva ROC ######################

# Entrenar el clasificador DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)
y_scores = classifier.predict_proba(X_test)[:, 1]

# Calcular la curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)

# Graficar la curva ROC
plt.figure()
plt.plot(fpr, tpr, color='blue', lw=2, label='Curva ROC (área = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tasa de Falsos Positivos')
plt.ylabel('Tasa de Verdaderos Positivos')
plt.title('Curva ROC (Clasificador DecisionTreeClassifier)')
plt.legend(loc="lower right")
plt.show()