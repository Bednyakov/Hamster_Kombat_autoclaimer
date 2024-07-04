import requests
from core.loggers import logger
from config import HamsterKombat

def get_status_daily_reward() -> bool:
    url = "https://api.hamsterkombat.io/clicker/list-tasks"

    response = requests.post(url, headers=HamsterKombat.headers)

    if response.status_code == 200:
        try:
            data = response.json()
            for task in data["tasks"]:
                if task["id"] == "streak_days":
                    return task["isCompleted"]
        
        except ValueError as e:
            logger.error(f"Ответ не в формате JSON: {e}")


def claim_daily_reward() -> None:
    if get_status_daily_reward() is False:
        url = "https://api.hamsterkombat.io/clicker/check-task"
        payload = {"taskId": "streak_days"}

        response = requests.post(url, headers=HamsterKombat.headers, json=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                completed = data["task"]["isCompleted"]
                logger.info(f'Claim daily reward: {completed}')
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
