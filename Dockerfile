FROM python:3.9.1

ADD requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt && \
    rm -f /requirements.txt


ADD app /app

WORKDIR /app

CMD ["uvicorn","--host", "0.0.0.0", "--port","8000", "src.main:rest_app"]
