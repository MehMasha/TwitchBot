# import requests
# import os
# import json
# from dotenv import load_dotenv
# from twitchio.ext import commands


# load_dotenv()
# token = os.getenv('ACCESS_TOKEN')
# client_id = os.getenv('CLIENT_ID')

# res = requests.post(
#     f'https://api.twitch.tv/helix/moderation/bans?broadcaster_id=633244077&moderator_id=633244077',
#     headers={'Authorization': f'Bearer {token}', 'Client-Id': client_id, 'Content-Type': 'application/json'},
#     json={"data": {"user_id": "79474873", "reason": "stop pls", "duration": 15}}
#     )
# print(res.json())

# def p(*kwargs):
#     print(kwargs*2)

# p(12345)

# def sum_f():
#     global a
#     a = 100

# sum_f()
# print(a)
# from dotenv import load_dotenv
# import asyncio
# import os
# from twitchAPI.twitch import Twitch


# load_dotenv()
# token = os.getenv('ACCESS_TOKEN')
# client_id = os.getenv('CLIENT_ID')


# async def twitch_example():
#     # initialize the twitch instance, this will by default also create a app authentication for you
#     twitch = await Twitch(client_id, token)
#     user = await first(twitch.get_users(logins='mehmasha'))
#     # print the ID of your user or do whatever else you want with it
#     print(user.id)

# # run this example
# asyncio.run(twitch_example())


# print(hash("mehmasha"))
import pymongo

client = pymongo.MongoClient('mongodb://root:your_password@localhost:27017/')

db = client['twitch_bot']

collection = db['users']

# Добавление документа в коллекцию
new_document = {
    "name": "username2",
    "wins": 1,
}
collection.insert_one(new_document) 
new_document = {
    "name": "username1",
    "wins": 1,
}
collection.insert_one(new_document)

# Чтение всех документов из коллекции
documents = collection.find()

for document in documents:
    print(document)