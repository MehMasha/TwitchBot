from datetime import datetime
import pymorphy2


def get_followage(followed_at, ctx, morph, lang) -> str:
    follow_date = followed_at.replace(tzinfo=None)
    follow_time = int((datetime.now() - follow_date).total_seconds())
    times = {
        "год": follow_time // (3600 * 24 * 365),
        "день": follow_time // (3600 * 24) % 365,
        "час": follow_time // 3600 % 24,
        "минута": follow_time // 60 % 60,
        "секунда": follow_time % 60,
    }
    if lang == 'ru':
        res_str = f"@{ctx.author.name}, ты зафоловлен на меня уже: "
    else:
        res_str = f"@{ctx.author.name}, You've been following my channel for: "

    for key, value in times.items():
        if value:
            word = morph.parse(key)[0]
            word_skl = word.make_agree_with_number(value).word
            res_str += f"{value} {word_skl} "
    res_str += "SeemsGood"
    return res_str


def get_commands(lang) -> str:
    if lang == 'ru':
        res_str = "Команды: "
        res_str += "!followage - посмотреть сколько зафоловлен, "
        res_str += "!donate - донат, "
        res_str += "!tg - телеграм, "
        res_str += "!discord - дискорд, "
        res_str += "!boosty - эксклюзивный контент, "
        res_str += "!db - ссылка на мою айти историю, "
        res_str += "!рост - узнать рост стримера, "
        res_str += "!python - мой гайд Python, "
        res_str += "!games - список игр, которые у меня есть, "
        res_str += '!огурец - мой влог с праздника огурца'
    else:
        res_str = "Commands: "
        res_str += "!followage - how much you're following a channel, "
        res_str += "!donate - donate for more streams in english, "
        res_str += "!tg - alerts and chat, "
        res_str += "!discord - discord, "
        res_str += "!boosty - exclusive content, "
        res_str += "!db - video about my sad IT story, "
        res_str += "!рост - to khow streamer's height, "
        res_str += "!python - my python guide, "
    return res_str
