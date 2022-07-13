FROM python:3.10.2
COPY ./app /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r /app/requirements.txt
CMD ["python", "/app/main.py"]
