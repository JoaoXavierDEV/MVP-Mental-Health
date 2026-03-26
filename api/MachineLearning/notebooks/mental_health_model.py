
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import pickle

# Load dataset
url = "PUT_YOUR_DATASET_URL_HERE"
dataset = pd.read_csv(url)

# Preprocessing
dataset = dataset.drop(["Timestamp", "comments", "state"], axis=1, errors="ignore")

for col in dataset.columns:
    dataset[col].fillna(dataset[col].mode()[0], inplace=True)

def limpar_genero(g):
    g = str(g).lower()
    if "male" in g or g == "m":
        return "male"
    elif "female" in g or g == "f":
        return "female"
    else:
        return "other"

dataset["Gender"] = dataset["Gender"].apply(limpar_genero)
dataset["treatment"] = dataset["treatment"].map({"Yes": 1, "No": 0})

le = LabelEncoder()
for col in dataset.columns:
    dataset[col] = le.fit_transform(dataset[col])

# Split
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Model pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("SVM", SVC())
])

param_grid = {
    "SVM__C": [0.1, 1, 10],
    "SVM__kernel": ["linear", "rbf"]
}

grid = GridSearchCV(pipeline, param_grid, cv=5)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

# Evaluation
pred = best_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(best_model, f)
