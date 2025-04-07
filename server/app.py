#!/usr/bin/env python3
"""Websockets server with structured handlers and room management"""

import asyncio
import json
from websockets.asyncio.server import serve
import websockets

# Store rooms and their members
rooms = {}
websocket_info = {}  # Maps websocket to {'room_id': ..., 'username': ...}


async def handle_create(websocket, data):
    """Hanldes creation of a room"""
    new_room = data.get("room_id")
    username = data.get("username")

    if not new_room or not username:
        await send_error(websocket, "Missing room_id or username")
        return

    if new_room in rooms:
        await send_error(websocket, "Room already exists")
        return

    rooms[new_room] = {'members': set(), 'messages': {}}
    rooms[new_room]['members'].add(websocket)
    websocket_info[websocket] = {'room_id': new_room, 'username': username}
    await send_success(websocket, f"Created room {new_room}", new_room)
    await notify_room(new_room, {"type": "user_joined", "username": username})


async def notify_room(room_id, message):
    """Notifies a room and it's all users"""
    if room_id not in rooms:
        return
    for client in list(rooms[room_id]['members']):
        try:
            await client.send(json.dumps(message))
        except (websockets.exceptions.ConnectionClosedError,
                websockets.exceptions.ConnectionClosedOK):
            pass


async def handle_join(websocket, data):
    """Handles the join in a room"""
    requested_room = data.get("room_id")
    username = data.get("username")

    if not requested_room or not username:
        await send_error(websocket, "Missing room_id or username")
        return

    if requested_room not in rooms:
        await send_error(websocket, "Room does not exist")
        return

    rooms[requested_room]['members'].add(websocket)
    websocket_info[websocket] = {'room_id': requested_room, 'username': username}
    
    await send_success(websocket, f"Joined room {requested_room}", requested_room)
    await notify_room(requested_room, {"type": "user_joined", "username": username})


async def remove_user_from_room(websocket):
    """Removes a user from a room"""
    if websocket not in websocket_info:
        return

    room_id = websocket_info[websocket]['room_id']
    username = websocket_info[websocket]['username']

    if room_id in rooms:
        rooms[room_id]['members'].discard(websocket)
        await notify_room(room_id, {"type": "user_left", "username": username})
        
        # If the users set is empty, delete the room
        if not rooms[room_id]['members']:
            del rooms[room_id]

    del websocket_info[websocket]


async def handle_send(websocket, data):
    """Handles the sending functionality"""
    # {} in the get is the value to return if it doesn't exist
    room_id = websocket_info.get(websocket, {}).get('room_id') if websocket in websocket_info else None
    message = data.get("message")
    message_id = data.get("message_id")
    username = websocket_info.get(websocket, {}).get('username')

    if not all([room_id, message, message_id, username]):
        await send_error(websocket, "Invalid request parameters")
        return

    if room_id not in rooms:
        await send_error(websocket, "Room not found")
        return

    if websocket not in rooms[room_id]['members']:
        await send_error(websocket, "Not a member of this room")
        return

    rooms[room_id]['messages'][message_id] = {
        'sender': username,
        'content': message,
        'received': False,
    }

    await notify_room(room_id, {
        "type": "message",
        "message_id": message_id,
        "username": username,
        "content": message
    })


async def handle_receive(websocket, data):
    """Handle the recipt of the message"""
    room_id = websocket_info.get(websocket, {}).get('room_id')
    message_id = data.get("message_id")
    username = websocket_info.get(websocket, {}).get('username')

    if not all([room_id, message_id, username]):
        await send_error(websocket, "Invalid request parameters")
        return

    if room_id not in rooms or message_id not in rooms[room_id]['messages']:
        await send_error(websocket, "Message not found")
        return

    message = rooms[room_id]['messages'][message_id]
    if username != message['sender']:
        message['received'] = True
        await websocket.send(json.dumps({
            "type": "received",
            "message_id": message_id
        }))


async def send_error(websocket, message):
    """Hanldes the error"""
    await websocket.send(json.dumps({"type": "error", "message": message}))


async def send_success(websocket, message, room_id=None):
    """Handles success"""
    response = {"type": "success", "message": message}
    if room_id:
        response["room_id"] = room_id
    await websocket.send(json.dumps(response))


async def handle_disconnect(websocket, _):
    """Handles disconnection"""
    await remove_user_from_room(websocket)
    username = websocket_info.get(websocket, {}).get('username', 'Unknown')
    await send_success(websocket, f"{username} disconnected")

ACTION_HANDLERS = {
    "join": handle_join,
    "create": handle_create,
    "send": handle_send,
    "disconnect": handle_disconnect,
    "received": handle_receive,
}


async def handler(websocket):
    """The handler of the websocket"""
    websocket_info[websocket] = {'room_id': None, 'username': None}
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action", "")
                if action not in ACTION_HANDLERS:
                    await send_error(websocket, "Invalid action")
                    continue
                await ACTION_HANDLERS[action](websocket, data)
            except json.JSONDecodeError:
                await send_error(websocket, "Invalid JSON format")
            except Exception as e:
                await send_error(websocket, f"Server error: {str(e)}")
    finally:
        await remove_user_from_room(websocket)


async def main():
    """Main function"""
    async with serve(handler, "localhost", 8765) as server:
        print("WebSocket server started")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
