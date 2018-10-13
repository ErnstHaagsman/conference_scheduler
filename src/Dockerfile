FROM python:3.7-slim-stretch

WORKDIR /opt/confsched/

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

CMD ["python3", \
     "manage.py", \
     "runserver", \
     "0.0.0.0:8000", \
     "--settings=confsched.settings.debug"]
