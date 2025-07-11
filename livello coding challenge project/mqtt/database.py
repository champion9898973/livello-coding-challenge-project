import sqlite3

def init_db():
    conn = sqlite3.connect('mqtt_data.db')
    cursor = conn.cursor()

    # Create Devices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Devices (
            device_id TEXT PRIMARY KEY,
            last_seen TEXT
        )
    ''')

    # Create Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            sensor_type TEXT,
            sensor_value REAL,
            timestamp TEXT,
            FOREIGN KEY (device_id) REFERENCES Devices(device_id)
        )
    ''')

    conn.commit()
    conn.close()

def store_valid_message(message):
    conn = sqlite3.connect('mqtt_data.db')
    cursor = conn.cursor()

    # Update or insert device info
    cursor.execute('''
        INSERT INTO Devices (device_id, last_seen) 
        VALUES (?, ?) 
        ON CONFLICT(device_id) 
        DO UPDATE SET last_seen=excluded.last_seen
    ''', (message['device_id'], message['timestamp']))

    # Insert into Events table
    cursor.execute('''
        INSERT INTO Events (device_id, sensor_type, sensor_value, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (
        message['device_id'],
        message['sensor_type'],
        message['sensor_value'],
        message['timestamp']
    ))

    conn.commit()
    conn.close()
