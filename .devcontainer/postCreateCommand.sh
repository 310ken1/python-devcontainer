#!/bin/sh
set -ex  # -e: エラーで停止, -x: コマンド出力

# 所有権変更
sudo mkdir -p /workspace/.venv
sudo chown -R vscode:vscode /workspace/.venv || true

# 実行環境のインストール
curl https://mise.run | sh
mise trust --all
mise install
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc

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
