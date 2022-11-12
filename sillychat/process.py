import random

from konlpy.tag import Okt

okt = Okt()


def get_blur_word(text):
    nouns = [word for word, word_type in okt.pos(text) if word_type == "Noun"]
    if "안녕" in text:
        nouns.append("안녕")

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
            message["content"] += " " + random.choice("😎🤐😜🤑😭🤬😡😈🧐☠🤔🥳")

    return [message]


def process_random_ban(message):
    if message["type"] == "message" and "blurWord" in message:
        if random.random() <= 0.05:
            return [
                message,
                {
                    "type": "ban",
                    "user": message["user"],
                    "reason": f"'{message['user']['name']}'님이 운영정책 위반으로 인해 1분간 채팅할 수 없습니다 !!! 🤬",
                },
            ]

    return [message]
