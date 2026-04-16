from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8694124474:AAFSPgMvgRlOKFiWC8ARdB1jnb8tMG4hkkQ"

USER_MAP = {
    "69ba04dd6dfc6f22c864f8f9": "你的TelegramChatID"
}

@app.route("/", methods=["GET"])
def home():
    return "Webhook running"

@app.route("/webhook", methods=["POST", "HEAD", "GET"])
def webhook():
    if request.method in ["GET", "HEAD"]:
        return "", 200

    data = request.json
    print(data)

    action = data.get("action", {})
    action_type = action.get("type")

    if action_type == "addMemberToCard":
        member_id = action["data"]["idMember"]
        card_name = action["data"]["card"]["name"]

        chat_id = USER_MAP.get(member_id)

        if chat_id:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"你有新的 Trello 任务：{card_name}"
                }
            )

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)