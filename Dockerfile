ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-alpine

ENV SERVER_URL=https://0.0.0.0:3000

WORKDIR /usr/src/integration_bot
COPY . .

RUN pip --no-cache-dir install -U pip -r requirements.txt
RUN apk add --no-cache ca-certificates

CMD ["python3", "-m", "integration_bot"]