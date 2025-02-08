# Fraud Detection System

![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)
![AWS RDS](https://img.shields.io/badge/Amazon_RDS-527FFF?style=for-the-badge&logo=amazon-rds&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

The **Fraud Detection System** is a real-time data pipeline designed to detect fraudulent banking transactions. It uses **Apache Kafka** for streaming data, **AWS RDS** for storing transaction data, and **Python** for processing and fraud detection logic. If a transaction is flagged as fraudulent, the system sends an email alert to the user.

---

## Features

- **Real-Time Fraud Detection**: Processes streaming transaction data in real-time using Kafka.
- **Data Storage**: Stores all transactions in an AWS RDS database, with a separate table for flagged fraudulent transactions.
- **Email Alerts**: Sends an email notification to the user if a transaction is flagged as fraudulent.
- **Scalable Architecture**: Built using Kafka for high-throughput and scalable data streaming.
- **Rule-Based Detection**: Implements customizable rules to identify fraudulent transactions (e.g., large amounts, unusual locations, etc.).

---

## Architecture

1. **Data Producer**: Generates synthetic bank transaction data and publishes it to a Kafka topic.
2. **Kafka Cluster**: Manages the streaming of transaction data between producers and consumers.
3. **Data Consumer**: Consumes transaction data from Kafka, processes it, and stores it in AWS RDS.
4. **Fraud Detection**: Applies fraud detection rules to identify suspicious transactions.
5. **AWS RDS**: Stores all transactions in a `transactions` table and flagged frauds in a `fraud_transactions` table.
6. **Email Alert System**: Sends email notifications to users for flagged transactions.

---

## Technologies Used

- **Apache Kafka**: For real-time data streaming.
- **AWS RDS**: For storing transaction data (e.g., PostgreSQL, MySQL).
- **Python**: For data generation, Kafka producers/consumers, and fraud detection logic.
- **SMTP**: For sending email alerts.
- **Confluent Kafka Python Client**: For interacting with Kafka.
- **Psycopg2**: For interacting with AWS RDS (PostgreSQL).

---

## Getting Started

### Prerequisites

- Python 3.10+
- Apache Kafka (or Confluent Cloud)
- AWS RDS instance (e.g., PostgreSQL)
- SMTP server for sending emails (e.g., Gmail, AWS SES)

### Installation

1. Clone the repository:
   ```bash
   git clone https://https://github.com/gopipandit/kafka_fraud_detection
   cd fraud-detection-system