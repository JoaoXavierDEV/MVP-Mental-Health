import sys
from pathlib import Path

# Garante que o diretorio api/ esta no path para os imports funcionarem
API_DIR = Path(__file__).resolve().parent.parent
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))
