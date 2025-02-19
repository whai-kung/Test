FROM python:3.13-slim-bookworm
# https://github.com/docker-library/python/blob/0330f0baedb296c8806a869d04fe76838f721647/3.13/slim-bookworm/Dockerfile

RUN apt-get update && \
  apt-get upgrade -y

RUN pip3 install poetry==1.8.4
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml

# Set the working directory
WORKDIR /app
COPY . /app

RUN poetry install --with dev --sync

# RUN VIRTUAL_ENV_DISABLE_PROMPT=1 source venv/bin/activate venv
RUN echo "PS1='\w: '" >> /root/.bashrc
RUN echo "export HISTCONTROL=ignoreboth:erasedups" >> /root/.bashrc

