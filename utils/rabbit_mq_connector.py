from typing import Callable, Any
import pika


def rabbit_mq_connector(queue: str) -> Callable:
    """
    Декортаор, открывающий соединение с rabbitMQ и отправляющий посылки в очередь
    :param queue: имя очереди, в которую отправляются посылки
    :return: возвращает функцию
    """

    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
                channel = connection.channel()
                channel.queue_declare(queue=queue)
                headers, body = function(*args, **kwargs)
                channel.basic_publish(exchange='', routing_key=queue,
                                      properties=headers, body=body)
        return wrapper
    return decorator
