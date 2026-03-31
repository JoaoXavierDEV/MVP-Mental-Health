from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import cross_val_score


class Avaliador:
    """Classe responsavel por avaliar o desempenho do modelo."""

    def avaliar(self, modelo, X_test, y_test):
        """Avalia o modelo com metricas de classificacao."""
        predicoes = modelo.predict(X_test)

        return {
            "acuracia": accuracy_score(y_test, predicoes),
            "recall": recall_score(y_test, predicoes, average="weighted"),
            "precisao": precision_score(y_test, predicoes, average="weighted"),
            "f1": f1_score(y_test, predicoes, average="weighted"),
        }

    def cross_validate(self, modelo, X, y, cv=5):
        """Realiza validacao cruzada e retorna a acuracia media."""
        scores = cross_val_score(modelo, X, y, cv=cv, scoring="accuracy")
        return {
            "media": scores.mean(),
            "desvio": scores.std()
        }
