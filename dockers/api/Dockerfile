FROM python:3.10

WORKDIR /usr/src

ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8808"]