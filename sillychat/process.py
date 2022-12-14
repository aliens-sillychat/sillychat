import random

from konlpy.tag import Okt

okt = Okt()


def get_blur_word(text):
    nouns = [word for word, word_type in okt.pos(text) if word_type == "Noun"]
    if "μλ" in text:
        nouns.append("μλ")

    if len(nouns) == 0:
        return None

    return random.choice(nouns)


def process_random_blur_word(message):
    if message["type"] == "message":
        blur_word = get_blur_word(message["content"])
        if blur_word is not None:
            message["blurWord"] = blur_word

    return [message]


def process_random_emoji(message):
    if message["type"] == "message":
        if random.random() <= 0.15:
            message["content"] += " " + random.choice("ππ€ππ€π­π€¬π‘ππ§β π€π₯³")

    return [message]


def process_random_ban(message):
    if message["type"] == "message" and "blurWord" in message:
        if random.random() <= 0.05:
            return [
                message,
                {
                    "type": "ban",
                    "user": message["user"],
                    "reason": f"'{message['user']['name']}'λμ΄ μ΄μμ μ± μλ°μΌλ‘ μΈν΄ 1λΆκ° μ±νν  μ μμ΅λλ€ !!! π€¬",
                },
            ]

    return [message]
