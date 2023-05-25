import asyncio
import websockets
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer


clients = set()

async def echo(websocket, path):
    clients.add(websocket)

    try:
        async for message in websocket:
            print(message)
            for client in clients:
                await client.send(message)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection to client {websocket.remote_address} closed: {e}")
    finally:
        clients.remove(websocket)


async def start_websocket_server():
    async with websockets.serve(echo, '140.116.245.172', 8764, ping_interval=None):
        await asyncio.Future()  # Keep the server running


def start_http_server():
    server = TCPServer(('140.116.245.172', 7771), SimpleHTTPRequestHandler)
    print("HTTP server running at http://140.116.245.172:8080")
    server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    websocket_server_task = loop.create_task(start_websocket_server())
    http_server_thread = loop.run_in_executor(None, start_http_server)

    try:
        loop.run_until_complete(websocket_server_task)
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
