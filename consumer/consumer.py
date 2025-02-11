from confluent_kafka import Consumer, KafkaError
import json
import time
from dotenv import load_dotenv
import os
import logging
import sys
sys.path.append("F:\\Data Engineering\\kafka_fraud_detection")
from database.connection import Connector

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Kafka configuration
def get_kafka_config():
    return {
        'bootstrap.servers': os.getenv("bootstrap_server"), 
        'security.protocol': 'SASL_SSL',    
        'sasl.mechanisms': 'PLAIN',     
        'sasl.username': os.getenv("api_key2"),     
        'sasl.password': os.getenv("api_secret2"),
        'group.id': 'ABS_Bank_Ltd',
        'auto.offset.reset': 'earliest',
    }

# Kafka topic
KAFKA_TOPIC = os.getenv("topic")

def consume_messages():
    """
    Consume messages from the Kafka topic and process them.
    """
    # Create a consumer instance
    consumer = Consumer(get_kafka_config())

    # Subscribe to the topic
    consumer.subscribe([KAFKA_TOPIC])
    logger.info("Listening to the messages.............")

    try:
        while True:
            # Poll for messages (wait up to 1 second)
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue  # No message received

            if msg.error():
                # Handle errors
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.info(f"End of partition reached {msg.partition()}")
                else:
                    logger.error(f"Consumer Error: {msg.error()}")
                continue

            try:
                # Decode the message value
                data = json.loads(msg.value().decode('utf-8'))
                logger.info(f"Received message: {data}")  # Log the received message

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    except KeyboardInterrupt:
        logger.info("Consumer stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Close the consumer gracefully
        consumer.close()
        logger.info("Kafka consumer closed.")

def main():
    """
    Main function to start the Kafka consumer.
    """
    logger.info("Starting Kafka consumer...")
    consume_messages()

if __name__ == "__main__":
    main()