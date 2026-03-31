import pandas as pd


class Carregador:
    """Classe responsavel por carregar dados."""

    def carrega_dados(self, url, atributos):
        """Carrega dados de uma URL e retorna um DataFrame."""
        return pd.read_csv(url, names=atributos, header=0, skiprows=0,
                           delimiter=",")

    def carrega_dados_csv(self, url):
        """Carrega dados de uma URL CSV diretamente."""
        return pd.read_csv(url)
