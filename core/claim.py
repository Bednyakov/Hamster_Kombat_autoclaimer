import requests
from time import time
from random import randint
from core.loggers import logger
from core.config import HamsterKombat


logger = logger


def claim(url_res: str, headers_res: dict, data: dict = None) -> None:
    """
    Функция для отправки POST-запроса синхронизации и клейма монет.
    """
    with requests.Session() as session:

        response = session.post(url=url_res, headers=headers_res, json=data)

        if response.status_code == 200:
            logger.info(f"Claim {url_res[8:]} Status code: {response.status_code }")

            try:
                data =  response.json()
                return data
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
                return None
        
        logger.error(f"Ошибка при отправке POST-запроса на клейм: {response.status_code, response.text}")
        return None


def timestamp() -> int:
    """
    Функция получаения таймштампа.
    """
    return int(time())


def hamster_tap():
    """
    Функция для отправки POST-запроса с количеством тапов в Hamster Kombat.
    """
    url = "https://api.hamsterkombat.io/clicker/tap"

    data = {
        "count": randint(501, 513),
        "availableTaps": 0,
        "timestamp": timestamp()
    }

    response = requests.post(url, headers=HamsterKombat.headers, json=data)

    if response.status_code == 200:
        logger.info(f"Tap ok! Status code: {response.status_code }")
        try:
            result = response.json()
            return result
        except ValueError as e:
            logger.error(f"Ответ не в формате JSON: {e}")
            return None

    logger.error(f"Ошибка при отправке POST-запроса на TAP: {response.status_code, response.text}")
    return None
    


