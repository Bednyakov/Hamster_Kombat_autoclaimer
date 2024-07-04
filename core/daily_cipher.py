import base64
import requests
from core.loggers import logger
from config import HamsterKombat


def daily_cipher_decode(cipher):
    cipher = cipher[:3] + cipher[4:]
    result = base64.b64decode(cipher).decode('utf-8')
    return result

def get_cipher() -> None:
    """
    Функция для отправки POST-запроса и получения серкетного слова дня.
    """
    url = "https://api.hamsterkombat.io/clicker/config"

    response = requests.post(url, headers=HamsterKombat.headers)

    if response.status_code == 200:
        try:
            data = response.json()
            cipher = data['dailyCipher']['cipher']
            claimed = data['dailyCipher']['isClaimed']

            if claimed is False:
                result = daily_cipher_decode(cipher)
                logger.info(f"Секретное слово дня расшифровано: {result}")
                morse = text_to_morse(result)
                claim_cipher(result)
                
            return None
        
        except ValueError as e:
            logger.error(f"Ответ не в формате JSON: {e}")
            return None

    logger.error(f"Ошибка при отправке POST-запроса на шифр: {response.status_code, response.text}")
    return None

def claim_cipher(cipher: str) -> None:
    """
    Функция для отправки POST-запроса с секретным словом.
    """
    url = "https://api.hamsterkombat.io/clicker/claim-daily-cipher"

    data = {
            "cipher": cipher,
            }

    response = requests.post(url, headers=HamsterKombat.headers, json=data)

    if response.status_code == 200:
        try:
            data = response.json()
            logger.info(f"{data.get('dailyCipher', 'Слово заклеймлено.')}")
            return None
        
        except ValueError as e:
            logger.error(f"Ответ не в формате JSON: {e}")
            return None

    logger.error(f"Ошибка при отправке POST-запроса на шифр: {response.status_code, response.text}")
    return None


def text_to_morse(text: str) -> str:
    morse_code = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": "/",
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "'": ".----.",
        "!": "-.-.--",
        "/": "-..-.",
        "(": "-.--.",
        ")": "-.--.-",
        "&": ".-...",
        ":": "---...",
        ";": "-.-.-.",
        "=": "-...-",
        "+": ".-.-.",
        "-": "-....-",
        "_": "..--.-",
        '"': ".-..-.",
        "$": "...-..-",
        "@": ".--.-.",
    }

    text = text.upper()
    result = ""
    for char in text:
        if char in morse_code:
            result += morse_code[char] + " "

    logger.info(f"Морзянка: {result}")        
    return result


if __name__ == '__main__':
    get_cipher()

