#Forces a python3.9 amd64
FROM python:3.9-alpine@sha256:281811c93dbf7b29719709c129230edfa1b10585d720f95c60363a358e49b62c
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD gunicorn app:app --bind 0.0.0.0:$PORT