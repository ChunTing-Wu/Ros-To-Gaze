import asyncio
import websockets

clients = set()

async def echo(websocket, path):
    clients.add(websocket)

    websocket.max_size = 1024

    try:
        async for message in websocket:
            for client in clients:
                await client.send(message)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection to client {websocket.remote_address} closed: {e}")
    finally:
        clients.remove(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8764))
asyncio.get_event_loop().run_forever()
