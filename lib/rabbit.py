import json
import pika
from os import getenv

from dotenv import load_dotenv

class RabbitHelper:

    def __init__(self) -> None:
        load_dotenv()
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=getenv('RABBITMQ_HOST'),
                credentials=pika.PlainCredentials(
                    getenv('RABBITMQ_USERNAME'),
                    getenv('RABBITMQ_PASSWORD')
                ),
                virtual_host=getenv('RABBITMQ_VHOST')
            )
        )

        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=getenv('RABBITMQ_EXCHANGE'),exchange_type='direct')


    def send(self, json_message: str) -> None:
        self.channel.basic_publish(exchange=getenv('RABBITMQ_EXCHANGE'),
            routing_key=getenv('RABBITMQ_QUEUE_KEY_NOTION'),
            body=json_message)

    def close(self) -> None:
        self.channel.close()

