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

# 環境変数
ENV LANG=ja_JP.UTF-8 \
    LC_ALL=ja_JP.UTF-8

# パッケージインストール
RUN --mount=type=cache,target=/var/cache/dnf \
    dnf update -y && dnf install -y \
    shadow-utils \
    libatomic \
    sudo \
    procps-ng \
    tar \
    unzip \
    git \
    findutils \
    graphviz \
    glibc-langpack-ja \
    ipa-gothic-fonts && \
    dnf clean all

# PlantUMLインストール
RUN curl -LsSf "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar" -o /usr/local/bin/plantuml.jar

# ユーザ設定
RUN groupadd -g ${GID} ${USER} && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER} && \
    chmod 0440 /etc/sudoers.d/${USER} && \
    mkdir -p ${HOME}/.cache && \
    chown -R ${UID}:${GID} ${HOME}

# プロジェクト設定
RUN mkdir -p /workspace && chown -R ${UID}:${GID} /workspace
ENV PATH="/workspace/scripts/:$PATH"

USER ${USER}
WORKDIR ${HOME}
