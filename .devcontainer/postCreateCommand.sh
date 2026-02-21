#!/bin/sh
set -ex  # -e: エラーで停止, -x: コマンド出力

# docker-compose.ymlマウントしたフォルダの所有権を変更
sudo chown -R vscode:vscode /workspace/.venv || true
sudo chown -R vscode:vscode /workspace/node_modules || true

# 実行環境のインストール
export MISE_NODE_GPG_VERIFY=false
curl https://mise.run | sh
mise trust --all
mise install
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc

# Python
# 依存関係を同期
if [ -f "uv.lock" ]; then
    uv sync --frozen --no-editable --no-install-project
else
    uv sync --no-editable --no-install-project
fi

# Node.js
npm install -g aws-cdk
