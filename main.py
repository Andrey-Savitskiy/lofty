from typing import Tuple
import pika
from pika import BasicProperties
from config import INPUT_FILE_NAME
from utils.rabbit_mq_connector import rabbit_mq_connector


@rabbit_mq_connector(queue='parser')
def getter_channel_links(channel: str) -> Tuple[BasicProperties, str]:
    print(channel.split('@')[-1])
    return pika.BasicProperties(headers={'channel_name': channel.split('@')[-1]}), channel


def main() -> None:
    with open(INPUT_FILE_NAME, 'r', encoding='utf-8') as file:
        channels_list = file.read().split('\n')

    for channel in channels_list:
        getter_channel_links(channel)


if __name__ == '__main__':
    main()
