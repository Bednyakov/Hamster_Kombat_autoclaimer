import time
from random import randint
from core.loggers import logger
from config import HamsterKombat
from core.daily_cipher import get_cipher
from core.claim import claim, hamster_tap
from core.daily_reward import claim_daily_reward


def main():
    """
    Функции клейма и тапа вызываются через заданные периоды.
    Функция проверки и клейма секретного слова Hamster Kombat вызывается вместе с клеймом монет.
    """
    hamster_claim_time = time.time()
    hamster_tap_time = time.time()

    hamster_periodicity = 3  #  Периодичность вызова функции клейма в часах для Hamster Kombat
    tap_periodicity = 1  #  Периодичность вызова функции протапывания Hamster Kombat

    while True:
        current_time = time.time()
        one_hour = randint(3600, 3900)

        if current_time >= hamster_claim_time:
            result = claim(HamsterKombat.url, HamsterKombat.headers)
            balance = result['clickerUser']['balanceCoins']
            availableTaps = result['clickerUser']['availableTaps']
            logger.info(f"Hamster balance: {balance} Available Taps: {availableTaps}")
            get_cipher()
            claim_daily_reward()
            hamster_claim_time = current_time + hamster_periodicity * one_hour

        if current_time >= hamster_tap_time:
            result = hamster_tap()
            balance = result['clickerUser']['balanceCoins']
            availableTaps = result['clickerUser']['availableTaps']
            logger.info(f"Hamster balance: {balance} Available Taps: {availableTaps}")
            hamster_tap_time = current_time + tap_periodicity * one_hour

        time.sleep(60)


if __name__ == "__main__":
    main()