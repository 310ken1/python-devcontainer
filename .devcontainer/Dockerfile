FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal

# パッケージインストール
RUN --mount=type=cache,target=/var/cache/dnf \
  dnf update -y && dnf install -y \
  sudo \
  tar \
   unzip \
   git \
   java \
   graphviz \
   ipa-gothic-fonts

# PlantUMLインストール
ARG PLANTUML_VERSION=1.2025.2
ARG plantuml="https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar"
RUN curl -LsSf ${plantuml} -o /usr/local/bin/plantuml.jar

# AWS CLI v2 のインストール
# https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp && /tmp/aws/install && \
    rm -rf /tmp/aws /tmp/awscliv2.zip

# プロジェクトマネージャ(uv)のインストール
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
ENV PATH="/root/.local/bin/:$PATH"
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# 作業ディレクトリを作成
WORKDIR /workspace

# プロジェクトのインストール
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    if [ -f "uv.lock" ]; then \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-editable; \
    else \
    uv sync --no-install-project --no-editable; \
    fi
