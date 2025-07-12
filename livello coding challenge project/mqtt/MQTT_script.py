import asyncio
from gmqtt import Client as MQTTClient
import json
import random
import logging
from jsonschema import validate, ValidationError
from database import init_db, store_valid_message
from datetime import datetime, timezone, timedelta
import os

# Constants
BROKER_HOST = os.environ.get("BROKER_HOST", "mqtt-broker")
TOPIC = '/devices/events'
PUBLISH_INTERVAL = 5  # in seconds

device_ids = ['device_01', 'device_02', 'device_03', 'device_04', 'device_05']
sensor_types = ['temperature', 'humidity', 'pressure', 'light', 'motion']
ist = timezone(timedelta(hours=5, minutes=30))

# 🛠 Ensure logging always writes to the script's folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'invalid_messages.log')
print(LOG_FILE)

# Schema definition
schema = {
    "type": "object",
    "properties": {
        "device_id": {"type": "string"},
        "sensor_type": {"type": "string"},
        "sensor_value": {"type": "number"},
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["device_id", "sensor_type", "sensor_value", "timestamp"]
}

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(message)s')

file_handler = logging.FileHandler(LOG_FILE, mode='a')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Generate a random message with occasional invalid data
def generate_message():
    message = {
        "device_id": random.choice(device_ids),
        "sensor_type": random.choice(sensor_types),
        "sensor_value": round(random.uniform(10.0, 100.0), 2),
        "timestamp": datetime.now(ist).isoformat()
    }

    # Introduce an invalid message 20% of the time
    if random.random() < 0.2:
        invalid_field = random.choice(['device_id', 'sensor_type', 'sensor_value', 'timestamp', 'missing_field'])

        if invalid_field == 'device_id':
            message["device_id"] = 12345  # invalid type
        elif invalid_field == 'sensor_type':
            message["sensor_type"] = None  # invalid type
        elif invalid_field == 'sensor_value':
            message["sensor_value"] = "high"  # invalid type
        elif invalid_field == 'timestamp':
            message["timestamp"] = "invalid-date-format"  # invalid format
        elif invalid_field == 'missing_field':
            message.pop(random.choice(["device_id", "sensor_type", "sensor_value", "timestamp"]), None)  # remove a required field

    return message

# Validate message schema
def validate_message(message: dict) -> bool:
    try:
        validate(instance=message, schema=schema)
        return True
    except ValidationError as e:
        logging.error(f"Invalid message: {json.dumps(message)} | Reason: {e.message}")
        for handler in logging.root.handlers:
            handler.flush()
        return False

# Handle incoming MQTT messages
def on_message(client, topic, payload, qos, properties):
    try:
        message = json.loads(payload)
        validate(instance=message, schema=schema)
        print(f"✅ Received valid message: {message}")
        store_valid_message(message)
        print("📦 Message stored in the database.\n")
    except (json.JSONDecodeError, ValidationError) as e:
        logging.error(f"Invalid message: {payload} | Reason: {str(e)}")
        for handler in logging.root.handlers:
            handler.flush()
        print("❌ Invalid message received. Check logs.\n")

# Loop to publish random messages
async def publish_random_messages(client):
    while True:
        msg = generate_message()
        if validate_message(msg):
            client.publish(TOPIC, json.dumps(msg), qos=1)
            print(f"📤 Published message:\n{json.dumps(msg, indent=2)}")
            print("✅ Message published successfully.\n")
        else:
            print("⚠️ Skipped publishing invalid message.\n")
        await asyncio.sleep(PUBLISH_INTERVAL)

# Main function
async def main():
    init_db()
    print("✅ Database initialized.\n")

    client = MQTTClient("mqtt-client")
    client.on_message = on_message

    await client.connect(BROKER_HOST)
    client.subscribe(TOPIC)
    print(f"📡 Subscribed to topic: {TOPIC}\n")

    await asyncio.gather(
        publish_random_messages(client)
    )

if __name__ == '__main__':
    asyncio.run(main())
