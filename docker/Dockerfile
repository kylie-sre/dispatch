FROM gcr.io/unity-ie-sre-isolated-test/dispatch:base
LABEL maintainer="sre@unity3d.com"
LABEL org.opencontainers.image.title="Dispatch API Server"
LABEL org.opencontainers.image.description="Docker image for serving the Dispatch API server"
LABEL org.opencontainers.image.url="https://dispatch.io/"
LABEL org.opencontainers.image.source="https://github.com/kylie-sre/dispatch"
LABEL org.opencontainers.image.vendor="Unity Tech."
LABEL org.opencontainers.image.authors="sre@unity3d.com"

COPY setup.py setup.cfg requirements-base.txt requirements-dev.txt README.md /dispatch/
ADD dispatch /dispatch/dispatch
RUN /venv/bin/pip install /dispatch && \
  mkdir /dispatch/static
