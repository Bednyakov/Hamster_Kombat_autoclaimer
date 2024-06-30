import os
from dotenv import load_dotenv


load_dotenv()


class HamsterKombat:
    token: str = os.getenv('HAMSTER_TOKEN', 'default_token_if_not_set')

    url: str = "https://api.hamsterkombat.io/clicker/sync"

    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {token}",
    }


class HotWallet:
    token: str = os.getenv('HOT_TOKEN', 'default_token_if_not_set')

    url: str = "https://api0.herewallet.app/api/v1/user/hot/claim"

    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        "Authorization": f"{token}",
        "Telegram-Data": f"user={os.getenv('TELEGRAM_DATA')}"
    }