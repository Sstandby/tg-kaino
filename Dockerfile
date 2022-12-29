FROM python:3.10.9-slim-buster

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requeriments.txt
RUN prisma generate

CMD ["python", "-m", "bot"]
