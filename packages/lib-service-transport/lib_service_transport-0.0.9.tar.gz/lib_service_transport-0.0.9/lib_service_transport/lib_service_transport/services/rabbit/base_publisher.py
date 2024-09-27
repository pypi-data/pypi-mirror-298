from abc import abstractmethod
from typing import Any

from pika import BasicProperties
from pika.exceptions import ChannelClosed

from .base_queue_agent import BaseQueueAgent


class BasePublisherRabbit(BaseQueueAgent):
    def __init__(self, settings: 'RabbitMQSettings'):
        """
            Инициализация класса
        :param settings: настройки сервера RabbitMQ
        """
        super().__init__(settings=settings)

        self._queue = None
        self._callback_queue = None

        self._correlation_id = None
        self._response = None

    def on_response(
            self,
            ch: 'BlockingChannel',  # noqa
            method: 'Basic.Deliver',  # noqa
            properties: 'BasicProperties',
            body: bytes,
    ) -> None:
        """Получение ответа от RPC сервера"""
        if self._correlation_id == properties.correlation_id:
            self._response = body

    def setup(self, exchange_name: str) -> None:
        """
        Настройка обменника (exchange), очереди (queue).
        """
        self._channel.exchange_declare(
            exchange=exchange_name,
            durable=True,
        )

        self._queue = self._channel.queue_declare(
            queue='',
            exclusive=True,
            durable=True,
        )
        self._callback_queue = self._queue.method.queue

        self._channel.basic_consume(
            queue=self._callback_queue,
            on_message_callback=self.on_response,
        )

    def run(self, exchange_name: str) -> None:
        """Подключение к серверу RabbitMQ и настройка обменника и очереди."""
        self.connect()
        self.setup(exchange_name=exchange_name)

    def check_exists_queue(self, queue_name) -> None:
        """Проверка наличия очереди (queue)."""
        try:
            self._channel.queue_declare(queue=queue_name, passive=True)
        except ChannelClosed:
            raise

    @abstractmethod
    def publish_message(self, **kwargs: str | int) -> Any:
        """Отправляет сообщения в RabbitMQ и возвращает ответ."""
        pass
