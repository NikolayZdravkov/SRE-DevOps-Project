FROM python:3.13-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt



FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local

COPY app/ app/
COPY migrations/ migrations/
COPY run.py .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]