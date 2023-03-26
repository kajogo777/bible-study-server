#FROM python:3
FROM python:3.7-slim

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    git \
    libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
COPY ./src /code/

ENV DJANGO_SETTINGS_MODULE=ch_app_server.settings
RUN  python manage.py collectstatic --noinput --clear

COPY ./wait-for-it.sh /wait-for-it.sh
COPY ./docker-entrypoint.sh /docker-entrypoint.sh

USER ${APP_USER}:${APP_USER}
ENTRYPOINT ["/docker-entrypoint.sh"]