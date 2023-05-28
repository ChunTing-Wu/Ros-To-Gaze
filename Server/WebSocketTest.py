import asyncio
import websockets
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

HOST_IP = "140.116.245.172"
clients = {}

async def echo(websocket, path):
    clients[websocket] = websocket.remote_address

    try:
        async for message in websocket:
            sender = websocket
            for client, address in clients.items():
                if client != sender:
                    asyncio.create_task(client.send(message))
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection to client {websocket.remote_address} closed: {e}")
    finally:
        del clients[websocket]


async def start_websocket_server():
    global HOST_IP
    async with websockets.serve(echo, HOST_IP, 8764, ping_interval=None):
        await asyncio.Future()  # Keep the server running


def start_http_server():
    global HOST_IP
    server = TCPServer((HOST_IP, 7771), SimpleHTTPRequestHandler)
    print("HTTP server running at", HOST_IP)
    server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    websocket_server_task = loop.create_task(start_websocket_server())
    http_server_task = loop.run_in_executor(None, start_http_server)

    try:
        loop.run_until_complete(asyncio.wait([websocket_server_task]))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()