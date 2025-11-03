#!/usr/bin/env bash
set -e

DOCS="docs/sphinx"

find ${DOCS} -maxdepth 1 -type f -name "*.rst" ! -name "index.rst" -delete

sphinx-build -b gettext ${DOCS} ${DOCS}/_build/gettext
(cd ${DOCS} && sphinx-intl update -p _build/gettext -l ja)

sphinx-apidoc -f -o ${DOCS} src --module-first
sphinx-build -b html -D language=ja ${DOCS} ${DOCS}/_build/ja
