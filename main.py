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


# logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

logger.add("main_log.log", rotation="50 MB")

morph = pymorphy2.MorphAnalyzer(lang='ru')


load_dotenv()
token = os.getenv('ACCESS_TOKEN')
client_id = os.getenv('CLIENT_ID')
channel_id = 633244077
channel_id = 179916073
headers = {
    'Authorization': f'Bearer {token}',
    'Client-Id': client_id,
    'Content-Type': 'application/json'
}


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=token, prefix='!', initial_channels=['mehmasha'])
        # self.wait_for_ready()
        self.game_active = False
        self.players = {}
        with open('data/people.json', 'r') as file:
            self.chat_people = json.load(file)


    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        self.hello.start()
        self.hello1.start()
        self.whofoll.start()


    async def event_message(self, message):
        if message.echo:
            return
        print(message.author, message.author.id, message.content)
        user = message.author
        me = await message.channel.user()
        k = await me.fetch_followers(token)
        self.chat_people[user.name] = self.chat_people.get(user.name, 0) + 1

        if 'начальник' in message.content.lower():
            await message.channel.send(f'Привет, @{message.author.name}! Если ты хочешь узнать историю про на4альника и базу данных, то напиши команду !db')
        elif any(word in message.content.lower() for word in ['tits', 'tittie', 'сиськи', 'siski', ' sisi', 'titts', 'титьки', 'буферa']):
            if not (user.is_broadcaster or user.is_mod or user.is_vip or user.is_subscriber):
                await message.channel.send(f'@{message.author.name}, чел, ты.....')
                res = requests.post(
                    f'https://api.twitch.tv/helix/moderation/bans?broadcaster_id=633244077&moderator_id=633244077',
                    headers=headers,
                    json={"data": {"user_id": message.tags.get('user-id'), "reason": "stop pls", "duration": 15}}
                )
        elif message.first:
            await message.channel.send(f'@{message.author.name}, хэлоу! Добро пожаловать на мой стрим! Фоловься, залетай в телегу и в дискорд! <3')

        await self.handle_commands(message)

    async def is_live(self):
        result = await self.fetch_streams(user_logins=['mehmasha'])
        return bool(result)

    @routines.routine(minutes=9)
    async def hello1(self):
        is_live = await self.is_live()
        if is_live:
            try:
                res_str = 'Команды: '
                res_str += '!followage - посмотреть сколько зафоловлен, '
                res_str += '!donate - ссылка на донат, '
                res_str += '!tg - ссылка на телеграм, '
                res_str += '!discord - ссылка на дискорд, '
                res_str += '!boosty - ссылка на бусти, '
                res_str += '!db - ссылка на историю про меня разработчика'
                
                channel = self.connected_channels[0]
                await channel.send(res_str)
            except:
                print('Заебало')

    @routines.routine(minutes=9)
    async def hello(self):
        await asyncio.sleep(180)
        is_live = await self.is_live()
        if is_live:
            try:
                res_str = 'Заходи в телеграм или дискорд, там будут оповещения о начале стримов! А еще подписывайся на бусти TehePelo'
                channel = self.connected_channels[0]
                await channel.send(res_str)
            except:
                print('Заебало')

    @commands.command(name='db')
    async def db(self, ctx: commands.Context):
        await ctx.send('https://youtu.be/SJCaExarFiQ')

    @commands.command(name='tg')
    async def tg(self, ctx: commands.Context):
        await ctx.send('https://t.me/mehmasha_twitch')

    @commands.command(name='boosty')
    async def boosty(self, ctx: commands.Context):
        await ctx.send('https://boosty.to/mehmasha')

    @commands.command(name='discord')
    async def discord(self, ctx: commands.Context):
        await ctx.send('https://discord.gg/SG3qgBtAyh')

    @commands.command(name='donate')
    async def donate(self, ctx: commands.Context):
        await ctx.send('https://www.donationalerts.com/r/mehmasha')

    @commands.command(name='followage')
    async def followage(self, ctx: commands.Context):
        user = await ctx.author.user()
        me = await ctx.channel.user()
        k = await user.fetch_follow(me, token)
        logger.info(f'{user.name} вызвал команду followage')
        if k:
            follow_date = k.followed_at.replace(tzinfo=None)
            follow_time = int((datetime.now() - follow_date).total_seconds())
            times = {
                'год': follow_time // (3600 * 24 * 365),
                'день': follow_time // (3600 * 24) % 365,
                'час': follow_time // 3600 % 24,
                'минута': follow_time // 60 % 60,
                'секунда': follow_time % 60,
            }
            res_str = f'@{ctx.author.name}, ты зафоловлен на меня уже: '

            for key, value in times.items():
                if value:
                    word = morph.parse(key)[0]
                    word_skl = word.make_agree_with_number(value).word
                    res_str += f'{value} {word_skl} '
            res_str += 'SeemsGood'
            await ctx.send(res_str)
        else:
            res_str = f'@{ctx.author.name}, а ты еще не зафоловился... BibleThump'
            await ctx.send(res_str)

    @commands.command(name='commands')
    async def command(self, ctx: commands.Context):
        res_str = '!followage - посмотреть сколько зафоловлен, '
        res_str += '!donate - ссылка на донат, '
        res_str += '!tg - ссылка на телеграм, '
        res_str += '!discord - ссылка на дискорд, '
        res_str += '!boosty - ссылка на бусти, '
        res_str += '!db - ссылка на историю про меня разработчика'
        await ctx.send(res_str)

    @commands.command(name='мойрост')
    async def height(self, ctx: commands.Context):
        res_str = 'Мой рост 148см. Хочешь узнать свой? Запускай команду !рост'
        await ctx.send(res_str)

    @commands.command(name='рост')
    async def your_heights(self, ctx: commands.Context):
        result = list(range(130, 160)) + list(range(160, 180)) * 5 + list(range(180, 210))
        random.seed(ctx.author.id * 4)
        height = random.choice(result)
        random.seed()
        if ctx.author.is_broadcaster:
            await ctx.send(f'@{ctx.author.name}, твой рост - 148 см')
        else:
            await ctx.send(f'@{ctx.author.name}, твой рост - {height} см')


    @commands.command(name='uptime')
    async def uptime(self, ctx: commands.Context):
        uptime = int(time.time() - start_time)
        times = {
            'год': uptime // (3600 * 24 * 365),
            'день': uptime // (3600 * 24) % 365,
            'час': uptime // 3600 % 24,
            'минута': uptime // 60 % 60,
            'секунда': uptime % 60,
        }
        res_str = f'Бот работает уже: '

        for key, value in times.items():
            if value:
                word = morph.parse(key)[0]
                word_skl = word.make_agree_with_number(value).word
                res_str += f'{value} {word_skl} '
        await ctx.send(res_str)

    @routines.routine(minutes=9)
    async def whofoll(self):
        await asyncio.sleep(360)
        is_live = await self.is_live()
        if is_live:
            async with aiohttp.ClientSession() as session:
                channel_name = 'mehmasha'
                # Получение списка зрителей
                viewers_url = f'https://tmi.twitch.tv/group/user/{channel_name}/chatters'
                async with session.get(viewers_url) as resp:
                    viewers_data = await resp.json()
                    viewers = set(viewers_data['chatters']['viewers'])

                followers = set()
                cursor = None
                while True:
                    follows_url = f'https://api.twitch.tv/helix/users/follows?to_id={channel_id}&first=100'
                    if cursor:
                        follows_url += f'&after={cursor}'
                    async with session.get(follows_url, headers=headers) as resp:
                        follows_data = await resp.json()
                        try:
                            cursor = follows_data['pagination'].get('cursor')
                            for follow in follows_data['data']:
                                followers.add(follow['from_name'].lower())
                        except:

                            cursor = None

                    if not cursor:
                        break

                unfollowers = list(viewers - followers)

                bots = [
                    'drapsnatt', 
                    'aliceydra', 
                    'anotherttvviewer', 
                    '01ella', 
                    'commanderroot',
                    'digitalinstinct',
                    'kattah',
                    'lurxx',
                    'tinarif'
                    ]
                unfollowers = [p for p in unfollowers if p not in bots]
                bad_people = random.sample(unfollowers, 3)
                channel = self.connected_channels[0]
                await channel.send(f'@{bad_people[0]}, @{bad_people[1]} и @{bad_people[2]}, вы почему еще на зафолловились???')

    @commands.command(name='startguess')
    async def startguess(self, ctx):
        if self.game_active:
            await ctx.send("Игра уже активна. Угадайте число!")
        else:
            if ctx.author.is_broadcaster or ctx.author.is_mod:
                self.target_number = random.randint(1, 500)
                self.game_active = True
                await ctx.send("Игра началась! Угадайте число от 1 до 500. Используйте !guess [число] для угадывания.")
            else:
                await ctx.send("Только модератор или стример может запустить игру!")
            
    @commands.command(name='guess')
    async def guess(self, ctx, number: int):
        if not self.game_active:
            await ctx.send("Игра еще не началась! Используйте !startguess, чтобы начать.")
            return
        author = ctx.author.name
        cur_time = time.time()
        if author not in self.players or cur_time - self.players[author] > 30: 
            self.players[author] = cur_time
            if number == self.target_number:
                self.game_active = False
                self.players = {}
                await ctx.send(f"Поздравляем, @{ctx.author.name}! Вы угадали число {self.target_number}!")
            elif number < self.target_number:
                await ctx.send(f"@{ctx.author.name}, ваше число слишком маленькое!")
            else:
                await ctx.send(f"@{ctx.author.name}, ваше число слишком большое!")
        else:
            await ctx.send(f"@{ctx.author.name}, подождите еще {int(30 - (cur_time - self.players[author]))} секунд")
    
    @commands.command(name='mescount')
    async def mescount(self, ctx):
        author = ctx.author.name
        count = self.chat_people.get(author, 0)
        await ctx.send(f"@{ctx.author.name}, ты отправил {count} сообщений!")

    async def on_shutdown(self):
        with open('data/people.json', 'w') as file:
            json.dump(self.chat_people, file)


start_time = time.time()
bot = Bot()
try:
    bot.run()
finally:
    bot.loop.run_until_complete(bot.on_shutdown())
    bot.loop.close()

