from typing import Any
import pika
from pika import BasicProperties
from pika.exceptions import StreamLostError
from config import RABBITMQ_HOST
from utils.db import create_db, set_connection_to_db, get_channel_id


def callback(ch: Any, method: Any, properties: BasicProperties, body: bytes) -> None:
    """
    Функция, сохраняющая информацию о видео в бд
    :param ch:
    :param method:
    :param properties: заголовки
    :param body: ссылка на канал
    :return:
    """

    link = body.decode('utf-8')
    video_id = link.split('=')[-1]
    channel_name = properties.headers['channel_name']
    connect, cursor = set_connection_to_db()

    channel_id = get_channel_id(cursor, channel_name)

    if not channel_id:
        cursor.execute(f"""
        INSERT INTO channel (name) VALUES ('{properties.headers['channel_name']}');
        """)
        channel_id = get_channel_id(cursor, channel_name)

    cursor.execute(f"""
            INSERT INTO video (video_id, channel_id, video_href) VALUES ('{video_id}', {channel_id[0]}, '{link}');
            """)

    connect.close()


def main() -> None:
    """
    Функция, запускающая слушатель очереди db
    """

    try:
        with pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST)) as connection:
            channel = connection.channel()
            channel.basic_consume(queue='db', on_message_callback=callback, auto_ack=True)

            create_db()
            print('---DB QUEUE RUNNING---')
            channel.start_consuming()
    except StreamLostError as error:
        print(error.__traceback__)
        main()


if __name__ == '__main__':
    main()
