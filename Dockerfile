FROM python:3.10-slim

# Аргументы сборки
ARG PROXY_USER
ARG PROXY_PASS
ARG PROXY_HOST
ARG PROXY_PORT

ENV PROXY_USER=$PROXY_USER
ENV PROXY_PASS=$PROXY_PASS
ENV PROXY_HOST=$PROXY_HOST
ENV PROXY_PORT=$PROXY_PORT

WORKDIR /usr/src/app

COPY requirements.txt ./
# Устанавливаем зависимости БЕЗ прокси
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# На этапе запуска генерируем прокси url и экспортируем переменные окружения
CMD sh -c '\
    PROXY_URL="http://$(python3 -c "import urllib.parse,os; \
        print(f\"{urllib.parse.quote(os.environ.get('PROXY_USER', ''))}:\
{urllib.parse.quote(os.environ.get('PROXY_PASS', ''))}@\
{os.environ.get('PROXY_HOST', '')}:{os.environ.get('PROXY_PORT', '')}\")")"; \
    export HTTP_PROXY="http://$PROXY_URL"; \
    export HTTPS_PROXY="http://$PROXY_URL"; \
    python frontend/main.py
