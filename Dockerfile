FROM public.ecr.aws/lambda/python:3.9

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requeriments.txt
RUN prisma generate

CMD ["python", "-m", "bot"]
