FROM python:3.11-buster
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
WORKDIR /app
CMD ["python", "/app/main.py"]
COPY main.py /app/
