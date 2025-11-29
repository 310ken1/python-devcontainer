#!/bin/sh
set -eux  # -e: エラーで停止, -u: 未定義変数禁止, -x: コマンド出力

# Python
# 仮想環境を作成
if [ ! -d ".venv" ]; then
  uv venv
  source .venv/bin/activate
  uv python install ${PYTHON_VERSION}
fi
# 依存関係を同期
if [ -f "uv.lock" ]; then
    uv sync --frozen --no-editable --no-install-project;
else
    uv sync --no-editable --no-install-project;
fi
# 仮想環境をアクティベート
if [ -f "${VIRTUAL_ENV}/bin/activate" ]; then
  . "${VIRTUAL_ENV}/bin/activate"
fi
