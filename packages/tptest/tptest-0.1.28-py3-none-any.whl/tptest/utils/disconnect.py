import json


# Disconnection Function
async def disconnect(websocket):
    try:
        # Send a disconnect message to the WebSocket server
        await websocket.send(json.dumps({'action': 'disconnect'}))

        # Close the WebSocket connection
        await websocket.close()
        return True
    except Exception:
        return False
