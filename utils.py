from datetime import datetime
import pymorphy2


def get_followage(followed_at, ctx, morph) -> str:
    follow_date = followed_at.replace(tzinfo=None)
    follow_time = int((datetime.now() - follow_date).total_seconds())
    times = {
        "год": follow_time // (3600 * 24 * 365),
        "день": follow_time // (3600 * 24) % 365,
        "час": follow_time // 3600 % 24,
        "минута": follow_time // 60 % 60,
        "секунда": follow_time % 60,
    }
    res_str = f"@{ctx.author.name}, ты зафоловлен на меня уже: "

    for key, value in times.items():
        if value:
            word = morph.parse(key)[0]
            word_skl = word.make_agree_with_number(value).word
            res_str += f"{value} {word_skl} "
    res_str += "SeemsGood"
    return res_str


def get_commands() -> str:
    res_str = "Команды: "
    res_str += "!followage - посмотреть сколько зафоловлен, "
    res_str += "!donate - донат, "
    res_str += "!tg - телеграм, "
    res_str += "!discord - дискорд, "
    res_str += "!boosty - эксклюзивный контент, "
    res_str += "!db - ссылка на мою айти историю, "
    res_str += "!рост - узнать рост стримера, "
    res_str += "!python - мой гайд Python"
    return res_str
