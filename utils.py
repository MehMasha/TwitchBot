from datetime import datetime


def get_commands(lang) -> str:
    if lang == 'ru':
        res_str = "Команды: "
        res_str += "!donate - донат, "
        res_str += "!tg - телеграм, "
        res_str += "!discord - дискорд, "
        res_str += "!boosty - эксклюзивный контент, "
        res_str += "!db - ссылка на мою айти историю, "
        res_str += "!рост - узнать рост стримера, "
        res_str += "!python - мой гайд Python, "
        res_str += "!games - список игр, которые у меня есть, "
        res_str += "!films - список фильмов, которые смотрели, "
        res_str += '!огурец - мой влог с праздника огурца, '
        res_str += '!uptime - сколько работает бот'
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
