#!/usr/bin/env bash
set -ex  # -e: エラーで停止, -x: コマンド出力

# docker-compose.ymlマウントしたフォルダの所有権を変更
sudo chown -R vscode:vscode /workspace/.venv || true
#sudo chown -R vscode:vscode /workspace/node_modules || true
sudo chmod 666 /var/run/docker.sock || true

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
    uv sync --frozen
else
    uv lock
    uv sync
fi

# Node.js
npm install -g aws-cdk
npm install -g @redocly/cli
npm install -g @asyncapi/cli
