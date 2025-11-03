"""."""

import importlib.machinery
import sys
from pathlib import Path

# -- Path setup -----------------------------------------------------
# プロジェクトルート(docs の一つ上)
project_root = Path(__file__).resolve().parents[2]

# Pythonのモジュール探索パスに追加
sys.path.insert(0, str(project_root / "src"))

# ネームスペースパッケージ対応 (PEP 420)
# __init__.py が無くてもインポートできるように設定
if not any(isinstance(finder, importlib.machinery.PathFinder) for finder in sys.meta_path):
    sys.meta_path.append(importlib.machinery.PathFinder)

# -- Project information --------------------------------------------
project = ""
author = ""
release = "1.0.0"

# -- General configuration ------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "ja"
locale_dirs = ["locale/"]
gettext_compact = False

# -- Options for HTML output ----------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]

# autodoc 設定
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False

master_doc = "index"
