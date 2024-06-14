import os
import pika
import logging
import pybreaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables for the message queue
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

# Establish a connection to the message queue
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# Declare the queue
QUEUE_NAME = "issues"
channel.queue_declare(queue=QUEUE_NAME)

# Circuit breaker configuration
circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=5,  # Maximum number of failures before opening the circuit
    reset_timeout=60  # Time in seconds to wait before trying again
)


@circuit_breaker
def consume_messages(callback):
    def on_message(channel, method, properties, body):
        logger.info(f"Received message: {body}")
        callback(body)

    channel.basic_consume(queue=QUEUE_NAME,
                          on_message_callback=on_message, auto_ack=True)

    logger.info("Starting to consume messages")
    channel.start_consuming()


def publish_message(message):
    try:
        channel.basic_publish(exchange='',
                              routing_key=QUEUE_NAME, body=message)
        logger.info(f"Sent message: {message}")
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Failed to publish message: {e}")
        circuit_breaker.fail()
