#!/usr/bin/env python3

"""Websockets server with structured handlers and room management"""

import asyncio
import json
from websockets.asyncio.server import serve
import websockets

# Store rooms and their members
rooms = {}
# Track which room each user is in
user_rooms = {}
# Track usernames for each connection
user_names = {}

async def send_error(websocket, message):
    """Send error message to client"""
    await websocket.send(json.dumps({
        "type": "error",
        "message": message
    }))

async def send_success(websocket, message, room_id=None):
    """Send success message to client"""
    response = {"type": "success", "message": message}
    if room_id:
        response["room_id"] = room_id
    await websocket.send(json.dumps(response))

async def notify_room(room_id, message):
    """Broadcast message to all members of a room"""
    if room_id in rooms:
        for client in list(rooms[room_id]):
            try:
                await client.send(json.dumps(message))
            except (websockets.exceptions.ConnectionClosedError, 
                    websockets.exceptions.ConnectionClosedOK):
                pass

async def remove_user_from_room(websocket):
    """Remove user from their current room and clean up"""
    if websocket not in user_rooms:
        return

    room_id = user_rooms[websocket]
    username = user_names.get(websocket, "Unknown User")
    
    rooms[room_id].discard(websocket)
    del user_rooms[websocket]
    if websocket in user_names:
        del user_names[websocket]

    await notify_room(room_id, {
        "type": "user_left",
        "username": username  # Changed from user_name
    })

    if not rooms[room_id]:
        del rooms[room_id]

async def handle_join(websocket, data):
    """Handle join room request"""
    requested_room = data.get("room_id")
    username = data.get("username")
    
    if not requested_room:
        await send_error(websocket, "Missing room_id for join action")
        return
    if not username:
        await send_error(websocket, "Missing username for join action")
        return
    if requested_room not in rooms:
        await send_error(websocket, "Room does not exist")
        return

    await remove_user_from_room(websocket)
    rooms[requested_room].add(websocket)
    user_rooms[websocket] = requested_room
    user_names[websocket] = username

    await send_success(websocket, f"Joined room {requested_room}", requested_room)
    await notify_room(requested_room, {
        "type": "user_joined",
        "username": username  # Changed from user_name
    })

async def handle_create(websocket, data):
    """Handle create room request"""
    new_room = data.get("room_id")
    username = data.get("username")
    
    if not new_room:
        await send_error(websocket, "Missing room_id for create action")
        return
    if not username:
        await send_error(websocket, "Missing username for create action")
        return
    if new_room in rooms:
        await send_error(websocket, "Room already exists")
        return

    rooms[new_room] = set()
    await remove_user_from_room(websocket)
    rooms[new_room].add(websocket)
    user_rooms[websocket] = new_room
    user_names[websocket] = username

    await send_success(websocket, f"Created room {new_room}", new_room)
    await notify_room(new_room, {
        "type": "user_joined",
        "username": username  # Changed from user_name
    })

async def handle_send(websocket, data):
    """Handle message sending to current room"""
    print(f"Data: {data}")
    if websocket not in user_rooms:
        await send_error(websocket, "Not in any room")
        return

    message = data.get("message")
    if not message:
        await send_error(websocket, "Missing message content")
        return

    room_id = user_rooms[websocket]
    username = user_names.get(websocket, "Unknown User")
    
    await notify_room(room_id, {
        "type": "message",
        "username": username,
        "content": message
    })


async def handle_disconnect(websocket, data):
    """Handle explicit disconnect request"""
    await remove_user_from_room(websocket)
    await send_success(websocket, "Disconnected from room")

ACTION_HANDLERS = {
    "join": handle_join,
    "create": handle_create,
    "send": handle_send,
    "disconnect": handle_disconnect
}


async def handler(websocket):
    """Main connection handler"""
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")

                print(f"Received action: {action}")  # Added this line

                if action not in ACTION_HANDLERS:
                    await send_error(websocket, "Invalid action")
                    continue

                await ACTION_HANDLERS[action](websocket, data)
            except json.JSONDecodeError:
                await send_error(websocket, "Invalid JSON format")
            except Exception as e:
                print(f"Error processing message: {e}")
                await send_error(websocket, f"Server error: {str(e)}")
    finally:
        await remove_user_from_room(websocket)


async def main():
    """Start the websocket server"""
    async with serve(handler, "localhost", 8765) as server:
        print("WebSocket server started")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
