from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name="fraud-detection-system",
    version="0.1.0",
    description="A system to detect fraudulent bank transactions using Kafka and Amazon RDS.",
    author="Gopi Nath Pandit",
    author_email="gopi_pandit@yahoo.com",
    url="https://https://github.com/gopipandit/kafka_fraud_detection",
    packages=find_packages(),  # Automatically find packages
    install_requires=get_requirements('requirements.txt'),  # Dependencies from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "start-producer=fraud_detection_system.producer.producer:main",
            "start-consumer=fraud_detection_system.consumer.consumer:main",
        ],
    }
)