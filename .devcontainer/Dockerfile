# syntax=docker/dockerfile:1.7
FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal

# 変数定義
# ユーザ設定
ARG USER=vscode
ARG UID=1001
ARG GID=1001
ARG HOME=/home/${USER}
# PlantUML
ARG PLANTUML_VERSION=1.2025.10
# Python
ARG PYTHON_VERSION=lts
# Node.js
ARG NODE_VERSION=lts

# 環境変数
ENV LANG=ja_JP.UTF-8 \
    LC_ALL=ja_JP.UTF-8 \
    PYTHON_VERSION=${PYTHON_VERSION}

# パッケージインストール
RUN --mount=type=cache,target=/var/cache/dnf \
    dnf update -y && dnf install -y \
    shadow-utils \
    sudo \
    procps-ng \
    tar \
    unzip \
    git \
    findutils \
    java-21-amazon-corretto-headless \
    graphviz \
    glibc-langpack-ja \
    ipa-gothic-fonts && \
    dnf clean all

# PlantUMLインストール
RUN curl -LsSf "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar" -o /usr/local/bin/plantuml.jar

# AWS CLI v2 のインストール
# https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp && /tmp/aws/install && \
    rm -rf /tmp/aws /tmp/awscliv2.zip

# ユーザ設定
RUN groupadd -g ${GID} ${USER} && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER} && \
    chmod 0440 /etc/sudoers.d/${USER} && \
    mkdir -p ${HOME} && \
    chown ${UID}:${GID} ${HOME}

# プロジェクト設定
RUN mkdir -p /workspace && chown -R ${UID}:${GID} /workspace
ENV PATH="/workspace/scripts/:$PATH"

USER ${USER}
WORKDIR ${HOME}

# Pythonプロジェクトマネージャ(uv)のインストール
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
ENV PATH="${HOME}/.local/bin/:${PATH}"
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Nodeバージョン管理ツール(nvs)のインストール
# https://github.com/jasongin/nvs
ENV NVS_HOME="${HOME}/.nvs" \
    PATH="${HOME}/.nvs:${PATH}"
RUN git clone https://github.com/jasongin/nvs "${NVS_HOME}"
RUN bash -c "\
    source ${NVS_HOME}/nvs.sh && nvs add ${NODE_VERSION} && nvs link ${NODE_VERSION}"
RUN echo '[ -s "$NVS_HOME/nvs.sh" ] && . "$NVS_HOME/nvs.sh" && nvs use' >> "${HOME}/.bashrc"
