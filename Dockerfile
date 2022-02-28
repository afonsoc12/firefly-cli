FROM python:3.7-alpine

ARG VERSION="n/a"

LABEL VERSION=${VERSION}

MAINTAINER Afonso Costa

ENV XDG_CONFIG_HOME=/config

WORKDIR /src

COPY . .

RUN ls -alh

RUN echo -e "def get_versions():\n    return {'version': '${VERSION}', 'full-revisionid': 'n/a', 'date': 'n/a', 'dirty': 'n/a', 'error': 'n/a'}" \
    > firefly_cli/_version.py

RUN pip install --upgrade pip && \
    #pip install -r requirements.txt && \
    pip install .

ENTRYPOINT [ "firefly-cli" ]