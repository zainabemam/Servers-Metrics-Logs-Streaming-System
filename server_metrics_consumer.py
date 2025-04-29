from kafka import KafkaConsumer
import sqlite3

# Kafka consumer setup
consumer = KafkaConsumer(
    'server-metrics',
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

# SQLite setup
conn = sqlite3.connect('server_metrics.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER,
        cpu INTEGER,
        mem INTEGER,
        disk INTEGER
    )
''')
conn.commit()

print("Listening for messages...")

try:
    for message in consumer:
        raw = message.value
        print("Received:", raw)

        try:
            # Convert string to dict
            parts = dict(pair.split(":") for pair in raw.split(","))
            data = {
                "id": int(parts["id"].strip()),
                "cpu": int(parts["cpu"].strip()),
                "mem": int(parts["mem"].strip()),
                "disk": int(parts["disk"].strip())
            }

            # Insert into DB
            cursor.execute('''
                INSERT INTO metrics (id, cpu, mem, disk)
                VALUES (:id, :cpu, :mem, :disk)
            ''', data)
            conn.commit()
            print("Saved to DB:", data)

        except Exception as e:
            print("Error processing message:", e)

except KeyboardInterrupt:
    print("Process interrupted, stopping...")

finally:
    consumer.close()
    conn.close()
    print("Kafka consumer and DB connection closed.")
