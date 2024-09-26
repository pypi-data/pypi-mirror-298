FROM python:3.9-slim

# Allow overriding of PyPI index URL and TLS certificates, required to install
# dependencies on CNES infra.
ARG PIP_INDEX_URL
ARG PIP_CERT

# Allow overriding package version based on Git repository state without installing git
# in the image.
ARG SETUPTOOLS_SCM_PRETEND_VERSION

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir .

ENTRYPOINT ["lgfk-cli"]
