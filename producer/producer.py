from confluent_kafka import Producer
import json
import time
from dotenv import load_dotenv
import os
import sys
sys.path.append("F:\\Data Engineering\\kafka_fraud_detection")
from data_generator.fake_data import FakeDataGenerator 

fake = FakeDataGenerator()

# Load environment variables
load_dotenv()

# Kafka configuration
conf = {
    'bootstrap.servers': os.getenv("bootstrap_server"), 
    'security.protocol': 'SASL_SSL',    
    'sasl.mechanisms': 'PLAIN',     
    'sasl.username': os.getenv("api_key2"),     
    'sasl.password': os.getenv("api_secret2"), 
}

# Create a producer instance
producer = Producer(conf)

# Topic to produce messages to
topic = os.getenv("topic")

# Delivery callback function
def delivery_callback(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

if __name__ == "__main__":
    try:
        for i in range(1, 5001):
            data = fake.generate_account_holder(i)
            try:
                producer.produce(topic, key=str(i), value=json.dumps(data), callback=delivery_callback)
            except Exception as e:
                print(f"Error producing message: {e}")
            time.sleep(0.001)
        
        # Flush messages to ensure all are sent
        producer.flush(timeout=10)  # Add a timeout to avoid indefinite blocking
        print("All messages sent to Kafka")
    except KeyboardInterrupt:
        print("Script interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.flush(timeout=10)  # Ensure all messages are sent before exiting