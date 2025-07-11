from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = 'mqtt_data.db'

# Utility function to query the SQLite database
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# 🔹 Endpoint to get all devices with their last seen timestamp
@app.route('/devices', methods=['GET'])
def get_devices():
    rows = query_db("""
        SELECT device_id, MAX(timestamp) as last_seen 
        FROM Events 
        GROUP BY device_id 
        ORDER BY last_seen DESC
    """)
    return jsonify([dict(row) for row in rows])

# 🔹 Endpoint to get last 10 events for a specific device
@app.route('/events/<device_id>', methods=['GET'])
def get_events(device_id):
    rows = query_db("""
        SELECT * FROM Events 
        WHERE device_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 10
    """, (device_id,))
    return jsonify([dict(row) for row in rows])

#  Use Flask default port 5000 instead of MQTT port (1883)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
