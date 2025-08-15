# Use multi-stage build for smaller image
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app
EXPOSE 8080
ENV PORT=8080
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]