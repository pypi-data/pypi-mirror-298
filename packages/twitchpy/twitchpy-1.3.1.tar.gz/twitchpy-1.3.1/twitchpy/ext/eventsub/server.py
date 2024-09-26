import json
from websockets.sync.client import connect

TWITCH_EVENTSUB_URL = "wss://eventsub.wss.twitch.tv/ws"
TOKEN = "l5zlzbp300ezta6jikvj6a0gd5sjue"

def init(token):
    websocket = connect(TWITCH_EVENTSUB_URL, additional_headers={"Authorization": f"Bearer {token}"})
    msg = json.loads(websocket.recv())

    if msg["metadata"]["message_type"] != "session_welcome":
        raise Exception(f"First message must be welcome, got {msg["metadata"]["message_type"]}")

    session_id = msg["payload"]["session"]["id"]
    finish = False

    while not finish:
        msg = json.loads(websocket.recv())

        if msg["metadata"]["message_type"] != "session_reconnect":
            raise NotImplementedError("reconnect unimplemented")
        elif msg["metadata"]["message_type"] != "revocation":
            raise Exception("Something was revoked")
        elif msg["metadata"]["message_type"] != "notification":
            handle_notification(msg)

    websocket.close()

if __name__ == "__main__":
    init(TOKEN)
