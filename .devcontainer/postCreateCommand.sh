#!/bin/sh
set -eux  # -e: エラーで停止, -u: 未定義変数禁止, -x: コマンド出力

# 所有権変更
sudo mkdir -p /workspace/.venv
sudo chown -R vscode:vscode /workspace/.venv || true
sudo mkdir -p /home/vscode/.cache/uv
sudo chown -R vscode:vscode /home/vscode/.cache/uv || true

# Pythonのインストール
uv python install ${PYTHON_VERSION}

# 仮想環境を作成
if [ ! -d ".venv" ]; then
  uv venv
fi

# 依存関係を同期
if [ -f "uv.lock" ]; then
    uv sync --frozen --no-editable --no-install-project
else
    uv sync --no-editable --no-install-project
fi
