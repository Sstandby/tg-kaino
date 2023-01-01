FROM python:3.10.9-slim-buster

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y git
RUN pip install -r requeriments.txt
RUN pip install git+https://github.com/coder2020official/pyTelegramBotAPI@botapi6.4
RUN prisma generate

CMD ["python", "-m", "bot"]
