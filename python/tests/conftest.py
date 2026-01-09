import sys
from pathlib import Path

# pytest の起動ディレクトリに依存せず、python/ を import 可能にする
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))