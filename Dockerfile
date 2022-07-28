ARG DOCKER_IMAGE=python:3.9-alpine \
    USER=nonroot \
    GROUP=nonroot \
    UID=1234 \
    GID=4321

# Install image
FROM $DOCKER_IMAGE AS install-image

WORKDIR /app

COPY . .

RUN apk add --no-cache tzdata git \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --user --no-cache-dir .

# Runtime image
FROM $DOCKER_IMAGE AS runtime-image

ARG USER \
    GROUP \
    UID \
    GID

ENV PATH="/home/.local/bin:$PATH" \
    XDG_CONFIG_HOME=/config \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /home $XDG_CONFIG_HOME \
    && addgroup --gid $GID $GROUP \
    && adduser -D -H --gecos "" \
                     --home "/home" \
                     --ingroup "$GROUP" \
                     --uid "$UID" \
                     "$USER" \
    && chown -R $USER:$GROUP /home $XDG_CONFIG_HOME \
    && rm -rf /tmp/* /var/{cache,log}/* /var/lib/apt/lists/*

USER nonroot
WORKDIR /home

COPY --from=install-image --chown=$USER:$GROUP /root/.local /home/.local

VOLUME /config

ENTRYPOINT ["firefly-cli"]
