import os
import asyncio
import requests
from dotenv import load_dotenv
from twitchio.ext import commands
from datetime import datetime
import pymorphy2
from twitchio.ext import routines
import random
import time
import json


lang = 'ru'

if lang == 'ru':
    from text_ru import *
else:
    from text_en import *

from utils import get_followage, get_commands

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
        # self.hello.start()
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
        # k = await me.fetch_followers(token)

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
                f"@{message.author.name}, {msg_first}"
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
                res_str = get_commands(lang)
                channel = self.connected_channels[0]
                await channel.send(res_str)
            except:
                print("Заебало")

    # @routines.routine(minutes=10)
    # async def hello(self):
    #     await asyncio.sleep(600)
    #     is_live = await self.is_live()
    #     if is_live:
    #         try:
    #             channel = self.connected_channels[0]
    #             await channel.send(routine_2)
    #         except:
    #             print("Заебало")

    @commands.command(name="db", aliases=["bd", "начальник", "DB", "Db", "Bd", "BD"])
    async def db(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - https://youtu.be/SJCaExarFiQ")
    @commands.command(name="огурец", aliases=["cucumber"])
    async def cucumber(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - Мой новый влог с Праздника Огурца - youtu.be/eHzFZWQftpA")

    @commands.command(name="python", aliases=["phyton", "питон", "пайтон"])
    async def python(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, {python_guide} - https://youtu.be/4z_nzaHgUhk")

    @commands.command(name="шорты", aliases=["shorts"])
    async def shorts(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, {youtube_shorts} - https://youtube.com/shorts/u8fYOWX0NgE?si=Fj62K7_5bx8ZGLlO")

    @commands.command(name="tg", aliases=["telegram", "TG", "Tg", "телеграмм", "телега", "тг"])
    async def tg(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, {tg_msg}")

    @commands.command(name="boosty")
    async def boosty(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - https://boosty.to/mehmasha")

    @commands.command(name="games")
    async def games(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - https://pastebin.com/LKFCNkKz")

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
        if k:
            res_str = get_followage(k.followed_at, ctx, morph, lang)
            await ctx.send(res_str)
        else:
            res_str = f"@{ctx.author.name}, {followage_msg}"
            await ctx.send(res_str)

    @commands.command(name="commands")
    async def command(self, ctx: commands.Context):
        res_str = get_commands(lang)
        await ctx.send(f"@{ctx.author.name}, - {res_str}")

    @commands.command(name="рост", aliases=["height"])
    async def height(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - {height_msg}")

    @commands.command(name="theme", aliases=["тема"])
    async def theme(self, ctx: commands.Context):
        await ctx.send(f"@{ctx.author.name}, - synthwave 84")

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
