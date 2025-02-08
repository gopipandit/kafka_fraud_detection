import os
from pathlib import Path

project_name = "fraud-detection-system"

list_of_files = [
    # Main package
    "__init__.py",
    "producer/__init__.py",
    "producer/producer.py",
    "consumer/__init__.py",
    "consumer/consumer.py",
    "fraud_detection/__init__.py",
    "fraud_detection/rules.py",
    "database/__init__.py",
    "database/connection.py",
    "utils/__init__.py",
    "utils/email_sender.py",
    "utils/helpers.py",    
    
    # Scripts
    "scripts/start_producer.sh",
    "scripts/start_consumer.sh",
    
    # Configuration and requirements
    "requirements.txt",
    "setup.py",
    "README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories if they don't exist
    if not filepath.exists():  # Check if the file already exists
        with open(filepath, "w", encoding="utf-8") as f:
            if filepath.name == "__init__.py":
                f.write("")  # Empty __init__.py file
            elif filepath.suffix == ".py":
                f.write(f"# {filepath.name}\n")  # Add a placeholder comment for Python files
            elif filepath.name == "README.md":
                f.write("# Fraud Detection System\n\nA system to detect fraudulent bank transactions using Kafka and Amazon RDS.\n")
            elif filepath.name == "requirements.txt":
                f.write("confluent-kafka==2.0.2\npsycopg2-binary==2.9.5\npython-dotenv==0.19.2\npytest==7.0.1\nsmtplib==0.0.1\n")
            elif filepath.name == "setup.py":
                f.write("""from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="fraud-detection-system",
    version="0.1.0",
    description="A system to detect fraudulent bank transactions using Kafka and Amazon RDS.",
    author="Gopi Nath Pandit",
    author_email="gopi_pandit@yahoo.com",
    url="https://https://github.com/gopipandit/kafka_fraud_detection",
    packages=find_packages(where="fraud_detection_system"),  
    package_dir={"": "fraud_detection_system"},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "start-producer=fraud_detection_system.producer.producer:main",
            "start-consumer=fraud_detection_system.consumer.consumer:main",
        ],
    },
)
""")
            elif filepath.suffix == ".sh":
                if filepath.name == "start_producer.sh":
                    f.write("#!/bin/bash\npython -m fraud_detection_system.producer.producer\n")
                elif filepath.name == "start_consumer.sh":
                    f.write("#!/bin/bash\npython -m fraud_detection_system.consumer.consumer\n")
        print(f"Created: {filepath}")
    else:
        print(f"{filepath} already exists.")