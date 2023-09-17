import os
import asyncio
import requests
from dotenv import load_dotenv
from twitchio.ext import commands
from datetime import datetime
import pymorphy2
import aiohttp
from loguru import logger
from twitchio.ext import routines
import random
import time
import json
import pymongo


from utils import get_followage, get_commands

# logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

logger.add("main_log.log", rotation="50 MB")

morph = pymorphy2.MorphAnalyzer(lang="ru")


load_dotenv()
token = os.getenv("ACCESS_TOKEN")
client_id = os.getenv("CLIENT_ID")
channel_id = 633244077
headers = {
    "Authorization": f"Bearer {token}",
    "Client-Id": client_id,
    "Content-Type": "application/json",
}
ban_words = ["tits", "tittie", "сиськи", "siski", " sisi", "titts", "титьки", "буферa"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=token, prefix="!", initial_channels=["mehmasha"])
        self.game_active = False
        self.players = {}
        # self.client = pymongo.MongoClient('mongodb://root:your_password@localhost:27017/')

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        self.hello.start()
        self.hello1.start()

    async def event_message(self, message):
        if message.echo:
            return
        print(message.author, message.author.id, message.content)
        print(message.tags)
        # 'custom-reward-id'
        if 'custom-reward-id' in message.tags:
            await self.process_reward(message)
        user = message.author
        me = await message.channel.user()
        k = await me.fetch_followers(token)

        if "несостоявш" in message.content.lower() or "не состоявш" in message.content.lower():
            await message.channel.send(
                f"Привет, @{message.author.name}! Если ты хочешь узнать подробную историю про мои страдания на работах в IT, то воспользуйся командой !db"
            )
        elif any(word in message.content.lower() for word in ban_words):
            if not (
                user.is_broadcaster or user.is_mod or user.is_vip or user.is_subscriber
            ):
                await message.channel.send(f"@{message.author.name}, чел, ты.....")
                new_user = await user.user()
                await me.timeout_user(token, channel_id, user.id, 15, "чел, ты...")

        elif message.first:
            await message.channel.send(
                f"@{message.author.name}, хэлоу! Добро пожаловать на мой стрим и в чат! Залетай в телегу и в дискорд! <3"
            )

        await self.handle_commands(message)

    async def process_reward(self, message):
        print(message.channel)
        print(message.author.name)
        print(message.tags)

        if message.tags['custom-reward-id'] == '22c8705a-7858-4f30-b10e-f64dd9a89e60':
            await self.toggle(message)
        if message.tags['custom-reward-id'] == '10ef79b1-1d69-41d6-97d2-09e641aa4357':
            await self.color(message)
        # 22c8705a-7858-4f30-b10e-f64dd9a89e60 -  toggle

    async def is_live(self):
        result = await self.fetch_streams(user_logins=["mehmasha"])
        return bool(result)

    @routines.routine(minutes=10)
    async def hello1(self):
        await asyncio.sleep(300)
        is_live = await self.is_live()
        if is_live:
            try:
                res_str = get_commands()
                channel = self.connected_channels[0]
                await channel.send(res_str)
            except:
                print("Заебало")

    @routines.routine(minutes=10)
    async def hello(self):
        await asyncio.sleep(600)
        is_live = await self.is_live()
        if is_live:
            try:
                res_str = "Заходи в телеграм или дискорд, там будут оповещения о начале стримов! А еще подписывайся на бусти TehePelo"
                channel = self.connected_channels[0]
                await channel.send(res_str)
            except:
                print("Заебало")

    @commands.command(name="db", aliases=["bd", "начальник", "DB", "Db", "Bd", "BD"])
    async def db(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - https://youtu.be/SJCaExarFiQ")

    @commands.command(name="python", aliases=["phyton", "питон", "пайтон"])
    async def python(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, мой гайд по питону - https://youtu.be/4z_nzaHgUhk")

    @commands.command(name="tg", aliases=["telegram", "TG", "Tg", "телеграмм", "телега", "тг"])
    async def tg(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, Алерты и кружочки - https://t.me/MehMashaAlerts Чатик - https://t.me/mehmasha_twitch")

    @commands.command(name="boosty")
    async def boosty(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - https://boosty.to/mehmasha")

    @commands.command(name="discord")
    async def discord(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - https://discord.gg/SG3qgBtAyh")

    @commands.command(name="donate", aliases=["донат", "Donate", "Донат"])
    async def donate(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - https://www.donationalerts.com/r/mehmasha")

    @commands.command(name="followage")
    async def followage(self, ctx: commands.Context):
        user = await ctx.author.user()
        me = await ctx.channel.user()
        k = await user.fetch_follow(me, token)
        logger.info(f"{user.name} вызвал команду followage")
        if k:
            res_str = get_followage(k.followed_at, ctx, morph)
            await ctx.send(res_str)
        else:
            res_str = f"@{ctx.author.name}, а ты еще не зафоловился... BibleThump"
            await ctx.send(res_str)

    @commands.command(name="commands")
    async def command(self, ctx: commands.Context):
        res_str = get_commands()
        await ctx.send(f"@{ctx.author.name}, - {res_str}")

    @commands.command(name="рост", aliases=["height"])
    async def height(self, ctx: commands.Context):
        res_str = "Мой рост 148см."
        # await ctx.send(res_str)
        await ctx.send(f"@{ctx.author.name}, - {res_str}")

    # @commands.command(name="рост", aliases=["height"])
    # async def your_heights(self, ctx: commands.Context):
    #     result = (
    #         list(range(140, 160)) + list(range(160, 180)) * 5 + list(range(180, 210))
    #     )
    #     random.seed(int(ctx.author.id) * 4 - datetime.now().day)
    #     height = random.choice(result)
    #     random.seed()
    #     if ctx.author.is_broadcaster:
    #         await ctx.send(f"@{ctx.author.name}, твой рост - 148 см")
    #     else:
    #         await ctx.send(f"@{ctx.author.name}, твой рост - {height} см")

    # @commands.command(name="член", aliases=["length", 'Член', 'писюн'])
    # async def your_dick(self, ctx: commands.Context):
    #     random.seed(2 * int(ctx.author.id) - datetime.now().day)
    #     if ctx.author.is_broadcaster:
    #         await ctx.send(f"@{ctx.author.name}, у тебя нет члена!")
    #     elif ctx.author.name.lower() == 'margot_tenebrae':
    #         await ctx.send(f"@{ctx.author.name}, члена нет, но есть яйца!")
    #     elif ctx.author.is_mod or ctx.author.is_vip or ctx.author.is_subscriber:
    #         result1 = (
    #             list(range(13, 15)) * 3 +  list(range(15, 20)) * 2 +  list(range(20, 30))
    #         )
    #         height = random.choice(result1)
    #         await ctx.send(f"@{ctx.author.name}, длина твоего члена - {height} см")
    #     else:
    #         result1 = (
    #             list(range(-3, 5)) + list(range(5, 10)) * 4 + list(range(10, 15)) * 6 +  list(range(15, 20)) * 2 +  list(range(20, 30))
    #         )
    #         height = random.choice(result1)
    #         await ctx.send(f"@{ctx.author.name}, длина твоего члена - {height} см")
    #     random.seed()

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        uptime = int(time.time() - start_time)
        times = {
            "год": uptime // (3600 * 24 * 365),
            "день": uptime // (3600 * 24) % 365,
            "час": uptime // 3600 % 24,
            "минута": uptime // 60 % 60,
            "секунда": uptime % 60,
        }
        res_str = f"Бот работает уже: "

        for key, value in times.items():
            if value:
                word = morph.parse(key)[0]
                word_skl = word.make_agree_with_number(value).word
                res_str += f"{value} {word_skl} "
        # await ctx.send(res_str)
        await ctx.send(f"@{ctx.author.name}, - {res_str}")

    @commands.command(name="startguess")
    async def startguess(self, ctx):
        if self.game_active:
            await ctx.send("Игра уже активна. Угадайте число!")
        else:
            if ctx.author.is_broadcaster or ctx.author.is_mod:
                self.target_number = random.randint(1, 500)
                self.game_active = True
                await ctx.send(
                    "Игра началась! Угадайте число от 1 до 500. Используйте !guess [число] для угадывания."
                )
            else:
                await ctx.send("Только модератор или стример может запустить игру!")

    @commands.command(name="guess")
    async def guess(self, ctx, number: int):
        if not self.game_active:
            await ctx.send(
                "Игра еще не началась! Используйте !startguess, чтобы начать."
            )
            return
        author = ctx.author.name
        cur_time = time.time()
        if author not in self.players or cur_time - self.players[author] > 30:
            self.players[author] = cur_time
            if number == self.target_number:
                self.game_active = False
                self.players = {}
                await ctx.send(
                    f"Поздравляем, @{ctx.author.name}! Вы угадали число {self.target_number}!"
                )
            elif number < self.target_number:
                await ctx.send(f"@{ctx.author.name}, ваше число слишком маленькое!")
            else:
                await ctx.send(f"@{ctx.author.name}, ваше число слишком большое!")
        else:
            await ctx.send(
                f"@{ctx.author.name}, подождите еще {int(30 - (cur_time - self.players[author]))} секунд"
            )

    @commands.command(name="mescount")
    async def mescount(self, ctx):
        author = ctx.author.name
        count = self.chat_people.get(author, 0)
        await ctx.send(f"@{ctx.author.name}, ты отправил {count} сообщений!")

    async def toggle(self, message):
        number = message.content
        author = message.author.name
        response = requests.get(f'http://192.168.1.68:5000/toggle/{number}')
        if response.text == 'wrong number':
            await message.channel.send(f"@{author}, такого пина нет!")
        elif response.text == 'on':
            await message.channel.send(f"@{author}, включаю!")
        elif response.text == 'off':
            await message.channel.send(f"@{author}, выключаю!")
        elif response.text == 'loh':
            new_user = await message.author.user()
            await me.timeout_user(token, channel_id, user.id, 15, "чел, ты...")
            await message.channel.send(f"@{author}, чел, ты все сжег!")

    async def color(self, message):
        author = message.author.name
        mes = message.content.split(',')
        response = requests.get(f'http://192.168.1.68:5000/arduino/{mes[0]}/{mes[1]}/{mes[2]}')
        await message.channel.send(f"@{author}, включаю!")

    @commands.command(name="pins")
    async def pins(self, ctx):
        author = ctx.author.name
        await ctx.send(f"@{ctx.author.name}, (10, 12, 14, 15, 17, 18, 21, 24, 26, 13, 19, 16)")




start_time = time.time()
bot = Bot()
while True:
    try:
        bot.run()
    finally:
        bot.loop.close()
