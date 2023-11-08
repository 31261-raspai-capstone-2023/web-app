FROM python:3.11-slim-buster

ENV TZ=Australia/Sydney

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./web_app /code/web_app

CMD ["python", "-um", "web_app.server"]