import asyncio
import websockets

# 儲存所有 WebSocket 連接的客戶端
clients = set()

async def echo(websocket, path):
    # 將客戶端加入 clients 集合
    clients.add(websocket)
    try:
        async for message in websocket:
            print(message,'received from client')
            # 將收到的資料發送給所有客戶端
            for client in clients:
                await client.send(message)
    finally:
        # 將客戶端從 clients 集合中移除
        clients.remove(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8764))
asyncio.get_event_loop().run_forever()
