from confluent_kafka import Consumer, KafkaError
import json
import time
from dotenv import load_dotenv
import os
import logging
import sys
sys.path.append("F:/Data Engineering/kafka_fraud_detection")
from database.connection import Connector

# from data_generator.fake_data import FakeDataGenerator 

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
        # 'auto.offset.reset': 'earliest',
    }

# Kafka topic
KAFKA_TOPIC = os.getenv("topic")

def insert_customer_data(connector, customer_data):
    """
    Insert customer data into the `customers` table.

    Args:
        connector (Connector): Instance of the Connector class.
        customer_data (dict): Customer data as a dictionary.
    """
    try:
        # Construct the INSERT query with embedded values
        query = f"""
        INSERT INTO kafka_bank.customers (user_id, name, address, phone_number, email, date_of_birth, account_number, account_type, balance)
        VALUES (
            {customer_data['user_id']},
            '{customer_data['name'].replace("'", "''")}',
            '{customer_data['address'].replace("'", "''")}',
            '{customer_data['phone_number']}',
            '{customer_data['email']}',
            '{customer_data['date_of_birth']}',
            '{customer_data['account_number']}',
            '{customer_data['account_type']}',
            {customer_data['balance']}
        );
        """
        
        # Execute the query
        print(query)
        connector.execute_query(query)
        logger.info(f"Inserted/Updated customer with user_id: {customer_data['user_id']}")
    except Exception as e:
        logger.error(f"Error inserting customer data: {e}")

def consume_messages():
    """
    Consume messages from the Kafka topic and process them.
    """
    # Create a consumer instance
    consumer = Consumer(get_kafka_config())

    # Subscribe to the topic
    consumer.subscribe([KAFKA_TOPIC])
    logger.info("Listening to the messages.............")

    # Initialize the Connector
    connector = Connector()

    try:
        while True:
            # Poll for messages (wait up to 1 second)
            msg = consumer.poll(timeout=0.001)
            
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
                customer_data = json.loads(msg.value().decode('utf-8'))
                logger.info(f"Received customer data: {customer_data}")

                # Insert the customer data into the database
                insert_customer_data(connector, customer_data)

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    except KeyboardInterrupt:
        logger.info("Consumer stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Close the consumer and database connection gracefully
        consumer.close()
        del connector  # Dispose of the Connector
        logger.info("Kafka consumer and database connection closed.")

if __name__ == "__main__":
    consume_messages()