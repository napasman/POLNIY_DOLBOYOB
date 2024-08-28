import asyncio
import websockets
import json


async def test():
    async with websockets.connect("ws://38.242.240.7:8000/ws") as websocket:
        print("Соединение открыто!")
        await websocket.send(
            json.dumps(
                {"keywords": ["or"]},  # тут указываем все кейворды, как в апи
                ensure_ascii=False,
            )
        )
        while 1:
            try:
                response = await websocket.recv()
                print(json.loads(response))
                return response
            except:
                print("Соединение зактыто!")
                break



