import asyncio
import json
import websockets

# Maps active username strings directly to their live websocket object
connected_users = {}

async def broadcast_user_list():
    """Sends an updated list of all online users to everyone connected."""
    if connected_users:
        payload = json.dumps({
            "type": "user_list",
            "users": list(connected_users.keys())
        })
        # Broadcast to all active sockets
        await asyncio.gather(*[user.send(payload) for user in connected_users.values()])

async def handle_client(websocket):
    username = None
    try:
        # Step 1: Wait for registration packet
        registration_data = await websocket.recv()
        data = json.loads(registration_data)
        
        if data.get("type") == "register":
            username = data.get("username")
            connected_users[username] = websocket
            print(f"User '{username}' logged into system.")
            await broadcast_user_list()
            
        # Step 2: Main packet distribution loop
        async for raw_message in websocket:
            msg = json.loads(raw_message)
            
            if msg.get("type") == "chat_message":
                target = msg.get("to")
                outbound_payload = json.dumps({
                    "type": "incoming_msg",
                    "from": username,
                    "text": msg.get("text")
                })
                
                # Direct routing to recipient if they are currently online
                if target in connected_users:
                    await connected_users[target].send(outbound_payload)
                    
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Step 3: Remove user when socket closes
        if username in connected_users:
            del connected_users[username]
            print(f"User '{username}' disconnected.")
            await broadcast_user_list()

async def main():
    print("WebSocket Server starting up on ws://localhost:8765...")
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
  
