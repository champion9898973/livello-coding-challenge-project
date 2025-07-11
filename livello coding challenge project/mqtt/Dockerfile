FROM python:3.10-slim

WORKDIR /app

COPY MQTT_script.py .
COPY requirements.txt .
COPY database.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "MQTT_script.py"]
