import pickle
from pathlib import Path

class Pipeline:
    
    def __init__(self):
        """Inicializa o pipeline"""
        self.pipeline = None

    def _resolve_path(self, path):
        """Resolve caminhos relativos a partir da pasta api."""
        path_obj = Path(path)
        if path_obj.is_absolute():
            return path_obj

        api_dir = Path(__file__).resolve().parents[1]
        return api_dir / path_obj
    
    def carrega_pipeline(self, path):
        """Carregamos o pipeline construído durante a fase de treinamento
        """

        pipeline_path = self._resolve_path(path)
        with open(pipeline_path, 'rb') as file:
            self.pipeline = pickle.load(file)
        return self.pipeline