FROM python:3.8-alpine

LABEL maintainer="Afonso Costa (@afonsoc12)"

ARG VERSION="n/a"
ENV XDG_CONFIG_HOME=/config
ENV TZ=Europe/Lisbon

LABEL VERSION=${VERSION}

WORKDIR /src

COPY . .

RUN apk update && \
    apk add tzdata && \
    echo -e "def get_versions():\n    return {'version': '${VERSION}', 'full-revisionid': 'n/a', 'date': 'n/a', 'dirty': 'n/a', 'error': 'n/a'}" \
    > firefly_cli/_version.py && \
    pip install --upgrade pip && \
    pip install .

VOLUME /config

CMD firefly-cli
