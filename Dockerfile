FROM python:3.13.7

WORKDIR /code
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY app ./app
COPY static ./static

ARG RELEASE
ENV RELEASE=$RELEASE

CMD ["python", "-m", "app.runner", "--path", "/city-simulation-service"]
