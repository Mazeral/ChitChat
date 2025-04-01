#!/usr/bin/env python3
"""Websockets server
This script creates a simple WebSocket echo server using the `websockets`
library.
It listens for incoming WebSocket connections on localhost port 8765.
For each connected client, it receives messages and sends the same message back.
The server runs indefinitely until manually stopped.
"""


import asyncio
from websockets.asyncio.server import serve


def handler(websocket):
    """Handler for the websocket
    websocket: The websocket object, handles sending and receices via websocket
    protocol.

    We receive the sent JSON data in string format because we need to serialize
    the data to string, then we deserialize it into a JSON format
    """


async def main():
    """Sets up and starts the WebSocket server.

    This asynchronous function initializes the WebSocket server using the
    `websockets.serve` function.
    It binds the `echo` function as the handler for incoming connections on
    the specified host ("localhost")
    and port (8765). Once the server is successfully started, it prints a
    confirmation message
    and then enters an infinite loop (`server.serve_forever()`) to keep the
    server running and listening for new connections and messages.
    """
    async with serve(echo, "localhost", 8765) as server:
        print("Websocket server started")
        await server.serve_forever()  # To make it run forever

if __name__ == "__main__":
    asyncio.run(main())
