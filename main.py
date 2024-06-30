import time
from claim import logger
from random import randint
from config import HotWallet, HamsterKombat
from claim import claim, hot_status, hamster_tap


def main():
    """
    Функции клейма и тапа вызываются через заданные периоды.
    """
    hot_claim_time = time.time()
    hamster_claim_time = time.time()
    hamster_tap_time = time.time()

    hot_periodicity = 4  #  Периодичность вызова функции клейма в часах для Hotwallet
    hamster_periodicity = 3  #  Периодичность вызова функции клейма в часах для Hamster Kombat
    tap_periodicity = 1  #  Периодичность вызова функции протапывания Hamster Kombat

    while True:
        current_time = time.time()
        one_hour = randint(3600, 3900)

        if current_time >= hot_claim_time:
            data = hot_status()
            result = claim(HotWallet.url, HotWallet.headers, data)
            balance = result['hot_in_storage']
            logger.info(f'HOT Wallet balance: {balance}')
            hot_claim_time = current_time + hot_periodicity * one_hour

        if current_time >= hamster_claim_time:
            result = claim(HamsterKombat.url, HamsterKombat.headers)
            balance = result['clickerUser']['balanceCoins']
            availableTaps = result['clickerUser']['availableTaps']
            logger.info(f"Hamster balance: {balance} Available Taps: {availableTaps}")
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