import os
import pickle
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


X,y = datasets.load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.8)

X_test_df = pd.DataFrame(X_test, columns = [f"X_test_{i}" for i in range(X_test.shape[1])])
y_test_df = pd.DataFrame(y_test, columns = ["target"])

df_test = pd.concat([X_test_df, y_test_df], axis = 1)

model_path = "models/"

if not os.path.exists(model_path):
    os.makedirs(model_path)

parameters = [
    {"clf": LogisticRegression(solver="liblinear", multi_class="ovr"), "name": f"{model_path}/binary-lr.joblib"},
    {"clf": Perceptron(eta0=0.1, random_state=0), "name": f"{model_path}/binary-percept.joblib"},
]

for param in parameters:
    clf = param["clf"]
    clf.fit(X_train, y_train)
    model_filename = f"{param['name']}"
    with open(model_filename, 'wb') as model_file:
        pickle.dump(clf, model_file)
    print(f"Model saved in {model_filename}")

# Simple Model Evaluation
model_path = 'models/binary-lr.joblib'
with open(model_path, 'rb') as model_file:
    loaded_model = pickle.load(model_file)

predictions = loaded_model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)