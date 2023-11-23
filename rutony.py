import json
from websockets.sync.client import connect
import time
import queue
from threading import Thread

def hello(q):
    with connect("ws://192.168.1.42:8383/Chat") as websocket:
        while True:
            message = websocket.recv()
            js = json.loads(message)
            text = js.get('text_text')
            username = js.get('user')
            user_id = js.get('user_id')
            site = js.get('site_cut')
            try:
                pass
                # if сообщение == донат с гудгейма, 
            except:
                pass
            time.sleep(1)


hello()