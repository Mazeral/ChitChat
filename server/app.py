#!/usr/bin/env python3

"""Websockets server with structured handlers and room management"""

import asyncio
import json
from websockets.asyncio.server import serve
import websockets
import uuid

# Store rooms and their members
rooms = {
    # room_id: {
    #     'members': set(websockets),
    #     'messages': {
    #         message_id: {
    #             'sender': username,
    #             'content': content,
    #             'seen_by': set(usernames)
    #         }
    #     }
    # }
}
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
        for client in list(rooms[room_id]['members']):  # Updated this line
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
    
    if room_id in rooms:
        rooms[room_id]['members'].discard(websocket)  # Updated this line
        del user_rooms[websocket]
        if websocket in user_names:
            del user_names[websocket]

        await notify_room(room_id, {
            "type": "user_left",
            "username": username
        })

        if not rooms[room_id]['members']:  # Updated this line
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
    if requested_room not in rooms:
        rooms[requested_room] = {'members': set(), 'messages': {}}  # Initialize properly
    rooms[requested_room]['members'].add(websocket)  # Updated this line
    user_rooms[websocket] = requested_room
    user_names[websocket] = username

    await send_success(websocket, f"Joined room {requested_room}", requested_room)
    await notify_room(requested_room, {
        "type": "user_joined",
        "username": username
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

    rooms[new_room] = {'members': set(), 'messages': {}}  # Initialize properly
    await remove_user_from_room(websocket)
    rooms[new_room]['members'].add(websocket)  # Updated this line
    user_rooms[websocket] = new_room
    user_names[websocket] = username

    await send_success(websocket, f"Created room {new_room}", new_room)
    await notify_room(new_room, {
        "type": "user_joined",
        "username": username
    })
# Modify handle_send function
async def handle_send(websocket, data):
    """Handle message sending to current room"""
    if websocket not in user_rooms:
        await send_error(websocket, "Not in any room")
        return

    message = data.get("message")
    message_id = data.get("message_id")
    if not message or not message_id:
        await send_error(websocket, "Missing message content or ID")
        return

    room_id = user_rooms[websocket]
    username = user_names.get(websocket, "Unknown User")
    
    # Store message in room history
    if room_id not in rooms:
        await send_error(websocket, "Room not found")
        return
    
    if 'messages' not in rooms[room_id]:
        rooms[room_id]['messages'] = {}
        
    rooms[room_id]['messages'][message_id] = {
        'sender': username,
        'content': message,
        'seen_by': set()
    }

    # Broadcast message to room
    await notify_room(room_id, {
        "type": "message",
        "message_id": message_id,
        "username": username,
        "content": message
    })

    # Send delivery confirmation to sender
    await websocket.send(json.dumps({
        "type": "message_ack",
        "message_id": message_id,
        "status": "delivered"
    }))


async def handle_disconnect(websocket, data):
    """Handle explicit disconnect request"""
    await remove_user_from_room(websocket)
    await send_success(websocket, "Disconnected from room")


# Add new handler for read confirmations
async def handle_read(websocket, data):
    """Handle read confirmation"""
    message_id = data.get("message_id")
    sender_ws = data.get("sender_ws")
    
    # Find sender's connection
    for conn in user_rooms:
        if str(conn.id) == sender_ws:
            await conn.send(json.dumps({
                "type": "read_confirmation",
                "message_id": message_id
            }))
            break


async def handle_mark_seen(websocket, data):
    """Handle marking messages as seen"""
    if websocket not in user_rooms:
        await send_error(websocket, "Not in any room")
        return

    room_id = user_rooms[websocket]
    username = user_names.get(websocket, "Unknown User")
    message_ids = data.get("message_ids", [])

    if room_id not in rooms or 'messages' not in rooms[room_id]:
        await send_error(websocket, "Room not found")
        return

    room = rooms[room_id]
    current_members = room['members']
    current_usernames = {user_names[ws] for ws in current_members if ws in user_names}

    updates = []
    for msg_id in message_ids:
        if msg_id in room['messages']:
            message = room['messages'][msg_id]
            message['seen_by'].add(username)
            
            if current_usernames.issubset(message['seen_by']):
                updates.append(msg_id)

    # Notify room about fully seen messages
    for msg_id in updates:
        await notify_room(room_id, {
            "type": "message_seen",
            "message_id": msg_id
        })

ACTION_HANDLERS = {
    "join": handle_join,
    "create": handle_create,
    "send": handle_send,
    "disconnect": handle_disconnect,
    'mark_seen': handle_mark_seen,
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
