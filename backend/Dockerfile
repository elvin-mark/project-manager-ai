FROM python:3.12-alpine

WORKDIR /backend

COPY app/ /backend/app/
COPY .env /backend/
COPY requirements.txt /backend/

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]