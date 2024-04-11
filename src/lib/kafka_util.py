from confluent_kafka import Producer, admin, error
import socket
import json


class KafkaConnection:
    def __init__(self, server, topic):
        if None in [server, topic]:
            raise ValueError("Invalid parameters")

        self.server = str(server)
        self.topic = str(topic)

        self.producer = Producer(
            {
                "bootstrap.servers": self.server,
                "client.id": socket.gethostname(),
            }
        )

        self.admin = admin.AdminClient(
            {
                "bootstrap.servers": self.server,
            }
        )

        # If not validated this will return an error, so we don't need to check
        # self.__verify_or_create_topic()

    def __verify_or_create_topic(self):
        topic_list = list()
        topic_list.append(admin.NewTopic(self.topic))
        print(self.admin.list_topics(topic=self.topic))
        if self.topic not in self.admin.list_topics():
            self.admin.create_topics(
                new_topics=topic_list,
                
            )

    def send(self, value):
        try:    
            self.producer.produce("shodan-asn-count", key='count', value=str(value))
            self.producer.flush()

        except error.KafkaError as e:
            return f"Error: {e}"
