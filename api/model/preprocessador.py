import pickle
from pathlib import Path
import numpy as np


class PreProcessador:
    """Classe responsavel por preprocessar novos dados para predicao."""

    def __init__(self):
        self.encoders = None
        self.features = None

    def _resolve_path(self, path):
        """Resolve caminhos relativos a partir da pasta api."""
        path_obj = Path(path)
        if path_obj.is_absolute():
            return path_obj

        api_dir = Path(__file__).resolve().parents[1]
        return api_dir / path_obj

    def carrega_encoders(self, encoders_path, features_path):
        """Carrega os encoders e a lista de features salvos durante o treinamento."""
        resolved_encoders_path = self._resolve_path(encoders_path)
        resolved_features_path = self._resolve_path(features_path)

        with open(resolved_encoders_path, "rb") as f:
            self.encoders = pickle.load(f)
        with open(resolved_features_path, "rb") as f:
            self.features = pickle.load(f)

    def limpar_genero(self, g):
        """Normaliza o campo genero."""
        g = str(g).strip().lower()
        if g in ["male", "m", "maile", "mal", "male (cis)", "make",
                  "male-ish", "cis male", "msle", "mail", "cis man", "man"]:
            return "Male"
        elif g in ["female", "f", "woman", "femake",
                    "cis female", "cis-female/femme", "female (cis)",
                    "female (trans)", "trans-female", "trans woman", "femail"]:
            return "Female"
        else:
            return "Other"

    def preparar_form(self, dados_dict):
        """Recebe um dicionario com os dados do formulario e retorna
        um array numpy pronto para predicao.
        """
        # Limpa o genero
        dados_dict["Gender"] = self.limpar_genero(dados_dict.get("Gender", ""))

        # Converte Age para string (LabelEncoder espera string)
        dados_dict["Age"] = str(dados_dict["Age"])

        encoded = []
        for col in self.features:
            valor = str(dados_dict.get(col, ""))
            encoder = self.encoders.get(col)
            if encoder is not None and valor in encoder.classes_:
                encoded.append(encoder.transform([valor])[0])
            else:
                # Valor desconhecido: usa 0 como fallback
                encoded.append(0)

        return np.array([encoded])

    def decodificar_target(self, valor_codificado):
        """Decodifica o valor predito para a classe original."""
        target_encoder = self.encoders.get("__target__")
        if target_encoder is not None:
            return target_encoder.inverse_transform([valor_codificado])[0]
        return str(valor_codificado)
