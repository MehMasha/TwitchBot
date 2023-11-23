import os
import asyncio
import requests
from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.ext import routines
import time


lang = 'ru'

if lang == 'ru':
    from text_ru import *
else:
    from text_en import *

from utils import get_commands, get_answer, get_rewards

load_dotenv()
token = os.getenv("ACCESS_TOKEN")

pointauc_token = os.getenv('POINTAUC_TOKEN')
pointauc_url = 'https://pointauc.com/api/oshino/bids'
pointauc_headers = {
    'Authorization': f'Bearer {pointauc_token}'
}


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=token, prefix="!", initial_channels=["mehmasha"])
        self.commands_file = open('commands.json')
        self.rewards_file = open('config.json')

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        self.hello1.start()

    async def event_message(self, message):
        if message.echo:
            if message.content == '!reload':
                self.rewards_file = open('config.json')
                self.commands_file = open('commands.json')

        print(message.author, message.author.id, message.content)
        # print(message.tags)
        if 'custom-reward-id' in message.tags:
            await self.process_reward(message)
        user = message.author
        me = await message.channel.user()

        if message.first:
            await message.channel.send(
                f"@{message.author.name}, {msg_first}"
            )

        if message.content[0] == '!':
            command = message.content[1:]
            answer = get_answer(self.commands_file, command, message.author.name, **vars)
            if answer:
                await message.channel.send(
                    answer
                )
                print('new')

        await self.handle_commands(message)

    async def process_reward(self, message):
        # print(message.tags['custom-reward-id'])
        rewards = get_rewards(self.rewards_file)
        if message.tags['custom-reward-id'] in rewards['auction_rewards']:
            auc_data = {
              "bids": [
                {
                  "cost": 10,
                  "username": message.tags.get('display-name'),
                  "message": message.content,
                  "color": message.tags.get('color', '#005500').lower(),
                  "isDonation": False,
                }
              ]
            }
            requests.post(pointauc_url, json=auc_data, headers=pointauc_headers)
            print(auc_data)

        if message.tags['custom-reward-id'] == '22c8705a-7858-4f30-b10e-f64dd9a89e60':
            await self.toggle(message)

    async def is_live(self):
        result = await self.fetch_streams(user_logins=["mehmasha"])
        return bool(result)

    @routines.routine(minutes=10)
    async def hello1(self):
        await asyncio.sleep(300)
        try:
            is_live = await self.is_live()
            if is_live:
                res_str = get_commands(lang)
                channel = self.connected_channels[0]
                await channel.send(res_str)
        except:
            print("Заебало")

    @commands.command(name="commands", aliases=['help', 'команды', 'помощь'])
    async def command(self, ctx: commands.Context):
        res_str = get_commands(lang)
        await ctx.send(f"@{ctx.author.name}, - {res_str}")

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        uptime = int(time.time() - start_time)
        times = {
            "г.": uptime // (3600 * 24 * 365),
            "д.": uptime // (3600 * 24) % 365,
            "ч.": uptime // 3600 % 24,
            "мин.": uptime // 60 % 60,
            "сек.": uptime % 60,
        }
        res_str = f"Бот работает уже: "

        for key, value in times.items():
            if value:
                res_str += f"{value} {key} "
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



start_time = time.time()
bot = Bot()
while True:
    try:
        bot.run()
    finally:
        bot.loop.close()
