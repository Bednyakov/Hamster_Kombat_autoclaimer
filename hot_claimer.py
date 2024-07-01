import os
import time
import logging
import requests
from claim import logger
from random import randint
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger('hot_logger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('hot_log.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class HotWallet:
    token: str = os.getenv('HOT_TOKEN', 'default_token_if_not_set')

    url: str = "https://api0.herewallet.app/api/v1/user/hot/claim"

    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        "Authorization": f"{token}",
        "Telegram-Data": f"user={os.getenv('TELEGRAM_DATA')}",
    }
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

    referrals_id = []


def hot_status():
    """
    Функция обновления данных в Hotwallet.
    """

    data = HotWallet.data
    url = "https://api0.herewallet.app/api/v1/user/hot/claim/status"

    response = requests.post(url, headers=HotWallet.headers, json=data)
    
    if response.status_code == 200:
        logger.info(f"Update Hot data. Status code: {response.status_code }")
        try:
            values = response.json()
            HotWallet.data['game_state']['last_claim'] = values['last_offchain_claim']
            HotWallet.data['game_state']['balance'] = values['hot_in_storage']
            referrals = get_referrals()
            HotWallet.data['game_state']["refferals"] = referrals["total_referals"]
            return HotWallet.data
        
        except ValueError as e:
            logger.error(f"Ответ не в формате JSON: {e}")
            return None

    logger.error(f"Ошибка при отправке POST-запроса на обновление Hot data: {response.status_code, response.text}")
    return None


def get_referrals() -> dict:
    """
    Функция обновления числа и списка рефералов.
    """
    url = "https://api0.herewallet.app/api/v1/user/hot/referrals"

    response = requests.get(url, headers=HotWallet.headers)

    if response.status_code == 200:
        try:
            values = response.json()
            total_referrals = values["total_referrals"]

            referrals_id = []

            for referral in values["referrals"]:
                referrals_id.append(referral["near_account_id"])
            HotWallet.referrals_id = referrals_id

            logger.info(f"Total referrals in HOT: {total_referrals}")
            return {"total_referals": total_referrals, "referals_id": referrals_id}
        
        except ValueError as e:
            logger.error(f"Ответ не в формате JSON: {e}")
            return None

    logger.error(f"Ошибка при отправке GET-запроса на обновление рефералов: {response.status_code, response.text}")
    return None


def notification() -> None:
    """
    Функция уведомления рефералов.
    """
    url = "https://api0.herewallet.app/api/v1/user/hot/notification"

    for id in HotWallet.referrals_id:

        data = {"friend_account_id": id}
        response = requests.post(url, headers=HotWallet.headers, json=data)

        if response.status_code == 200:
            logger.info(f"{id} notification.")
    
    return None


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


def main():
    """
    Функции клейма HOT.
    """
    hot_claim_time = time.time()

    hot_periodicity = 4  #  Периодичность вызова функции клейма в часах для Hotwallet

    while True:
        current_time = time.time()
        one_hour = randint(3600, 3900)

        if current_time >= hot_claim_time:
            data = hot_status()
            result = claim(HotWallet.url, HotWallet.headers, data)
            balance = result['hot_in_storage']
            logger.info(f'HOT Wallet balance: {balance}')
            notification()
            hot_claim_time = current_time + hot_periodicity * one_hour

        time.sleep(600)


if __name__ == "__main__":
    main()