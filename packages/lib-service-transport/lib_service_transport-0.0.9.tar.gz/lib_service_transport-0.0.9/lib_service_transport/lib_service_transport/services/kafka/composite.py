from typing import Iterable

from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka.admin import AdminClient
from confluent_kafka.admin import ClusterMetadata
from confluent_kafka.cimpl import NewTopic
from confluent_kafka.cimpl import KafkaException
from pydantic import BaseModel

from .base_consumer import BaseConsumerKafka


class CompositeKafka:
    consumers: dict[str, BaseConsumerKafka] = {}

    def __init__(self, consumer: Consumer):
        self._consumer = consumer
        self._running = True

    def add_consumer(
            self,
            event_type: str,
            consumer: BaseConsumerKafka,
    ) -> None:
        self.consumers[event_type] = consumer

    def get_handler(self, event_type: str) -> BaseConsumerKafka:
        try:
            return self.consumers[event_type]
        except KeyError:
            pass

    def subscribe_to_topics(self, topics: Iterable[str]) -> None:
        self._consumer.subscribe(topics)

    def create_topic(
            self,
            bootstrap_servers: str,
            topic_title: str,
            num_partitions: int = 1,
            replication_factor: int = 1,
    ) -> None:
        admin: ClusterMetadata = self._consumer.list_topics()

        if topic_title not in admin.topics:
            admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
            new_topic = NewTopic(topic_title, num_partitions, replication_factor)

            try:
                futures = admin_client.create_topics([new_topic])

                for topic, future in futures.items():
                    try:
                        future.result()
                    except Exception:
                        pass
            except Exception:
                pass  # TODO: log

    def consume_messages(self) -> None:

        while self._running:
            try:
                message = self._consumer.poll(timeout=1.0)

                if message is None:
                    continue
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        pass
                    elif message.error():
                        raise KafkaException(message.error())
                else:
                    event_type = message.key()
                    handler = self.get_handler(event_type.decode())
                    incoming_message = self.get_incoming_message(
                        value=message.value(),
                        incoming_message_schema=handler.incoming_message_schema,
                    )
                    handler.on_request(incoming_message=incoming_message)
            except Exception:
                pass

    def close_connection(self) -> None:
        self._consumer.close()

    def shutdown(self):
        self._running = False

    @classmethod
    def get_incoming_message(
            cls,
            value: bytes,
            incoming_message_schema: BaseModel,
    ) -> BaseModel:
        try:
            return incoming_message_schema.model_validate_json(value)
        except Exception:
            pass
