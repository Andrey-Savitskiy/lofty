from typing import Any, Tuple
from pika import BasicProperties
from pika.exceptions import StreamLostError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pika
from config import RABBITMQ_HOST, CHROME_DRIVER_PATH
from utils.rabbit_mq_connector import rabbit_mq_connector


@rabbit_mq_connector(queue='db')
def send_link_to_db(headers: BasicProperties, body: str) -> Tuple[BasicProperties, str]:
    return headers, body


def callback(ch: Any, method: Any, properties: BasicProperties, body: bytes) -> None:
    """
    Функция, парсящая ссылки всех видео на странице
    :param ch:
    :param method:
    :param properties: заголовки
    :param body: ссылка на канал
    :return:
    """

    channel = body.decode('utf-8')

    webdriver_service = Service(CHROME_DRIVER_PATH)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    driver.get(channel)
    driver.implicitly_wait(2)

    result_set = set()
    container = driver.find_element(By.XPATH, '//*[@id="contents"]')
    links_list = container.find_elements(By.XPATH, '//a[starts-with(@href,"/watch?v=")'
                                                   'and not(contains(@href, "&"))]')
    for link in links_list:
        link_text = link.get_attribute('href')
        if link_text not in result_set:
            result_set.add(link_text)
            send_link_to_db(headers=properties, body=link_text)

    driver.quit()


def main() -> None:
    """
    Функция, запускающая слушатель очереди parser
    """

    try:
        with pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST)) as connection:
            channel = connection.channel()
            channel.basic_consume(queue='parser', on_message_callback=callback, auto_ack=True)

            print('---PARSER QUEUE RUNNING---')
            channel.start_consuming()
    except StreamLostError as error:
        print(error)
        main()


if __name__ == '__main__':
    main()
