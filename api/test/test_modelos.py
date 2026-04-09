import pytest
import pickle
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

# --- Configuracao ---
BASE_DIR = Path(__file__).resolve().parent.parent
PIPELINE_PATH = BASE_DIR / "MachineLearning" / "pipelines" / "pipeline.pkl"
ENCODERS_PATH = BASE_DIR / "MachineLearning" / "models" / "encoders.pkl"
FEATURES_PATH = BASE_DIR / "MachineLearning" / "models" / "features.pkl"
DATASET_URL = "https://github.com/user-attachments/files/26290783/survey.csv"

# Thresholds minimos de desempenho
ACURACIA_MINIMA = 0.70
RECALL_MINIMO = 0.65
PRECISAO_MINIMA = 0.65
F1_MINIMO = 0.65


@pytest.fixture(scope="module")
def modelo():
    """Carrega o modelo treinado."""
    with open(PIPELINE_PATH, "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="module")
def encoders():
    """Carrega os encoders."""
    with open(ENCODERS_PATH, "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="module")
def features():
    """Carrega a lista de features."""
    with open(FEATURES_PATH, "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="module")
def dados_teste(encoders, features):
    """Prepara os dados de teste a partir do dataset original."""
    dataset = pd.read_csv(DATASET_URL)
    dataset = dataset.drop(
        ["Timestamp", "comments", "state", "Country"], axis=1, errors="ignore"
    )

    for col in dataset.columns:
        dataset[col] = dataset[col].fillna(dataset[col].mode()[0])

    def limpar_genero(g):
        g = str(g).strip().lower()
        if g in ["male", "m", "maile", "mal", "male (cis)", "make",
                  "male-ish", "cis male", "msle", "mail", "cis man",
                  "man", "ostensibly male, unsure what that really means",
                  "something kinda male?"]:
            return "Male"
        elif g in ["female", "f", "woman", "femake",
                    "cis female", "cis-female/femme", "female (cis)",
                    "female (trans)", "trans-female", "trans woman", "femail"]:
            return "Female"
        else:
            return "Other"

    dataset["Gender"] = dataset["Gender"].apply(limpar_genero)
    dataset = dataset[(dataset["Age"] > 15) & (dataset["Age"] < 100)]

    target_col = "treatment"
    X = dataset[features].copy()
    y = dataset[target_col].copy()

    # Aplica os mesmos encoders do treinamento
    for col in X.columns:
        le = encoders.get(col)
        if le is not None:
            X[col] = X[col].astype(str).apply(
                lambda v: le.transform([v])[0] if v in le.classes_ else 0
            )

    target_encoder = encoders.get("__target__")
    y = target_encoder.transform(y)

    # Usa a mesma seed para obter o mesmo split
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    return X_test, y_test


class TestModeloDesempenho:
    """Testes de desempenho do modelo de machine learning."""

    def test_acuracia_acima_do_minimo(self, modelo, dados_teste):
        """Verifica se a acuracia do modelo esta acima do threshold."""
        X_test, y_test = dados_teste
        predicoes = modelo.predict(X_test)
        acuracia = accuracy_score(y_test, predicoes)
        assert acuracia >= ACURACIA_MINIMA, (
            f"Acuracia {acuracia:.4f} abaixo do minimo {ACURACIA_MINIMA}"
        )

    def test_recall_acima_do_minimo(self, modelo, dados_teste):
        """Verifica se o recall do modelo esta acima do threshold."""
        X_test, y_test = dados_teste
        predicoes = modelo.predict(X_test)
        recall = recall_score(y_test, predicoes, average="weighted")
        assert recall >= RECALL_MINIMO, (
            f"Recall {recall:.4f} abaixo do minimo {RECALL_MINIMO}"
        )

    def test_precisao_acima_do_minimo(self, modelo, dados_teste):
        """Verifica se a precisao do modelo esta acima do threshold."""
        X_test, y_test = dados_teste
        predicoes = modelo.predict(X_test)
        precisao = precision_score(y_test, predicoes, average="weighted")
        assert precisao >= PRECISAO_MINIMA, (
            f"Precisao {precisao:.4f} abaixo do minimo {PRECISAO_MINIMA}"
        )

    def test_f1_acima_do_minimo(self, modelo, dados_teste):
        """Verifica se o F1-score do modelo esta acima do threshold."""
        X_test, y_test = dados_teste
        predicoes = modelo.predict(X_test)
        f1 = f1_score(y_test, predicoes, average="weighted")
        assert f1 >= F1_MINIMO, (
            f"F1-score {f1:.4f} abaixo do minimo {F1_MINIMO}"
        )


class TestModeloPredicao:
    """Testes de predicao do modelo."""

    def test_predicao_retorna_classe_valida(self, modelo, dados_teste):
        """Verifica se as predicoes sao classes validas (0 ou 1)."""
        X_test, _ = dados_teste
        predicoes = modelo.predict(X_test)
        assert set(predicoes).issubset({0, 1}), (
            f"Classes invalidas encontradas: {set(predicoes)}"
        )

    def test_predicao_unica_amostra(self, modelo, encoders, features):
        """Verifica se o modelo consegue predizer uma unica amostra."""
        # Simula uma entrada de formulario
        amostra = {}
        for col in features:
            le = encoders.get(col)
            if le is not None:
                amostra[col] = le.transform([le.classes_[0]])[0]
            else:
                amostra[col] = 0

        X_input = np.array([list(amostra.values())])
        predicao = modelo.predict(X_input)
        assert len(predicao) == 1
        assert predicao[0] in [0, 1]
