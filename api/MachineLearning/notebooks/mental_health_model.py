import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import pickle
import os

# --- Carga dos dados ---
url = "https://github.com/user-attachments/files/26290783/survey.csv"
dataset = pd.read_csv(url)

# --- Pre-processamento ---
# Remove colunas desnecessarias
dataset = dataset.drop(["Timestamp", "comments", "state", "Country"], axis=1, errors="ignore")

# Preenche valores ausentes com a moda
for col in dataset.columns:
    dataset[col] = dataset[col].fillna(dataset[col].mode()[0])


# Limpeza do campo Gender
def limpar_genero(g):
    g = str(g).strip().lower()
    if g in ["male", "m", "male ", "maile", "mal", "male (cis)", "make",
             "male-ish", "cis male", "msle", "mail", "cis man",
             "man", "ostensibly male, unsure what that really means",
             "male ", "something kinda male?", "male ", "male"]:
        return "Male"
    elif g in ["female", "f", "woman", "femake",
               "cis female", "cis-female/femme", "female (cis)",
               "female (trans)", "trans-female", "trans woman",
               "femail", "female"]:
        return "Female"
    else:
        return "Other"


dataset["Gender"] = dataset["Gender"].apply(limpar_genero)

# Filtra idades invalidas
dataset = dataset[(dataset["Age"] > 15) & (dataset["Age"] < 100)]

# --- Separacao de features e target ---
target_col = "treatment"
feature_cols = [col for col in dataset.columns if col != target_col]

X = dataset[feature_cols].copy()
y = dataset[target_col].copy()

# --- Label Encoding ---
encoders = {}
for col in X.columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le

# Codifica o target
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)
encoders["__target__"] = target_encoder

# --- Separacao treino/teste (holdout 80/20) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# --- Modelagem com 4 algoritmos ---
models = {
    "KNN": {
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier())
        ]),
        "params": {
            "knn__n_neighbors": [3, 5, 7, 9],
            "knn__weights": ["uniform", "distance"]
        }
    },
    "DecisionTree": {
        "pipeline": Pipeline([
            ("tree", DecisionTreeClassifier(random_state=42))
        ]),
        "params": {
            "tree__max_depth": [3, 5, 10, None],
            "tree__min_samples_split": [2, 5, 10]
        }
    },
    "NaiveBayes": {
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("nb", GaussianNB())
        ]),
        "params": {
            "nb__var_smoothing": [1e-9, 1e-8, 1e-7]
        }
    },
    "SVM": {
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("svm", SVC())
        ]),
        "params": {
            "svm__C": [0.1, 1, 10],
            "svm__kernel": ["linear", "rbf"]
        }
    }
}

results = {}
best_score = 0
best_model_name = None
best_model = None

print("=" * 60)
print("Treinamento e avaliacao dos modelos")
print("=" * 60)

for name, config in models.items():
    print(f"\n--- {name} ---")
    grid = GridSearchCV(
        config["pipeline"],
        config["params"],
        cv=5,
        scoring="accuracy",
        n_jobs=-1
    )
    grid.fit(X_train, y_train)

    y_pred = grid.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    cv_scores = cross_val_score(grid.best_estimator_, X_train, y_train, cv=5)

    results[name] = {
        "best_params": grid.best_params_,
        "cv_mean": cv_scores.mean(),
        "cv_std": cv_scores.std(),
        "test_accuracy": test_accuracy
    }

    print(f"  Melhores parametros: {grid.best_params_}")
    print(f"  Acuracia CV (treino): {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"  Acuracia (teste): {test_accuracy:.4f}")

    if test_accuracy > best_score:
        best_score = test_accuracy
        best_model_name = name
        best_model = grid.best_estimator_

# --- Resumo comparativo ---
print("\n" + "=" * 60)
print("Resumo comparativo")
print("=" * 60)
for name, res in results.items():
    marker = " << MELHOR" if name == best_model_name else ""
    print(f"  {name}: teste={res['test_accuracy']:.4f} | CV={res['cv_mean']:.4f}{marker}")

print(f"\nMelhor modelo: {best_model_name} (acuracia={best_score:.4f})")

# --- Exportacao do modelo ---
script_dir = os.path.dirname(os.path.abspath(__file__))
pipelines_dir = os.path.join(script_dir, "..", "pipelines")
models_dir = os.path.join(script_dir, "..", "models")

os.makedirs(pipelines_dir, exist_ok=True)
os.makedirs(models_dir, exist_ok=True)

pipeline_path = os.path.join(pipelines_dir, "pipeline.pkl")
encoders_path = os.path.join(models_dir, "encoders.pkl")
features_path = os.path.join(models_dir, "features.pkl")

with open(pipeline_path, "wb") as f:
    pickle.dump(best_model, f)
print(f"\nPipeline salvo em: {pipeline_path}")

with open(encoders_path, "wb") as f:
    pickle.dump(encoders, f)
print(f"Encoders salvos em: {encoders_path}")

with open(features_path, "wb") as f:
    pickle.dump(list(feature_cols), f)
print(f"Features salvos em: {features_path}")
