import logging
import requests
from time import time
from random import randint
from config import HotWallet, HamsterKombat


logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('my_log.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


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


data = {
        "game_state": 
        {
            "refferals": 27,
            "inviter": "null",
            "village": "85691.village.hot.tg",
            "last_claim": 1719654627885544200,
            "firespace": 2,
            "boost": 14,
            "storage": 22,
            "balance": 131760190
        }
    }

def hot_status():
    """
    Функция обновления данных в Hotwallet.
    """

    global data
    url = "https://api0.herewallet.app/api/v1/user/hot/claim/status"

    response = requests.post(url, headers=HotWallet.headers, json=data)
    
    if response.status_code == 200:
        logger.info(f"Update Hot data. Status code: {response.status_code }")
        try:
            values = response.json()
            data['game_state']['last_claim'] = values['last_offchain_claim']
            data['game_state']['balance'] = values['hot_in_storage']
            return data
        
        except ValueError as e:
            logger.error(f"Ответ не в формате JSON: {e}")
            return None

    logger.error(f"Ошибка при отправке POST-запроса на обновление Hot data: {response.status_code, response.text}")
    return None


def timestamp():
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
    


