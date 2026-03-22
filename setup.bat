@echo off

for /f "delims=" %%i in ('wsl wslpath -u "%cd:\=/%"') do (
  echo SAM_DOCKER_VOLUME_BASEDIR='%%i/api-mock/.aws-sam/build' > .devcontainer/.env.generated
)
