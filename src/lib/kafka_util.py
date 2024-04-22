from confluent_kafka import Producer, Consumer, admin, error
import socket
import json 

class KafkaConnection:
    """
    A class representing a connection to Apache Kafka.

    Parameters:
        server (str): The Kafka server address.
        topic (str): The Kafka topic to interact with.
    """
    def __init__(self, server, topic):
        """
        Initialize the KafkaConnection instance.

        Parameters:
            server (str): The Kafka server address.
            topic (str): The Kafka topic to interact with.
        """
        if None in [server, topic]:
            raise ValueError("Invalid parameters")

        self.server = str(server)
        self.topic = str(topic)
        self.producer = None
        self.consumer = None
        self.admin = None

    def _create_producer(self):
        """
        Create a Kafka Producer instance.
        """
        if self.producer is None:
            self.producer = Producer(
                {
                    "bootstrap.servers": self.server,
                    "client.id": socket.gethostname(),
                }
            )

    def _create_consumer(self):
        """
        Create a Kafka Consumer instance.
        """
        if self.consumer is None:
            self.consumer = Consumer(
                {
                    "bootstrap.servers": self.server,
                    "group.id": "shodan-etl",
                    "auto.offset.reset": "earliest",
                }
            )

            # Subscribe to topic
            self.consumer.subscribe([self.topic])

    def _create_admin_client(self):
        """
        Create a Kafka AdminClient instance.
        """
        if self.admin is None:
            self.admin = admin.AdminClient(
                {
                    "bootstrap.servers": self.server,
                }
            )

    def send(self, value, key):
        """
        Send a message to the Kafka topic.

        Parameters:
            value (str): The message to send.
        """
        if self.producer is None:
            self._create_producer()

        try:
            json_value = json.dumps(value)

            self.producer.produce(self.topic, key=key, value=json_value)
            self.producer.flush()

        except error.KafkaError as e:
            return f"Error: {e}"

    def poll_message(self, timeout_ms=1000):
        """
        Poll for a message from the Kafka topic.

        Parameters:
            timeout_ms (int): The maximum time to block waiting for a message, in milliseconds.

        Returns:
            str: The received message, or None if no message was received within the timeout.
        """
        if self.consumer is None:
            self._create_consumer()
        
        messages = self.consumer.poll(timeout_ms)
        messages = messages.value().decode('utf-8')
        
        if messages is None: 
            return None
        
        messages = json.loads(messages)

        # Return message if exists
        return messages