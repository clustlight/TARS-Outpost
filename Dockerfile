FROM python:3.11.3-slim-bullseye AS builder

COPY requirements.txt /

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt


FROM gcr.io/distroless/python3-debian11 AS runner

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/dotenv /usr/lib/python3.11/site-packages/dotenv
COPY --from=builder /usr/local/bin/uvicorn /usr/lib/python3.11/site-packages/uvicorn

ENV PYTHONPATH=/usr/lib/python3.11/site-packages

WORKDIR app/
COPY ./*.py /app/

ENTRYPOINT ["python", "main.py"]