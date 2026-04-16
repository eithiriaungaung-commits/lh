from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8694124474:AAFSPgMvgRlOKFiWC8ARdB1jnb8tMG4hkkQ"

USER_MAP = {
    "layhlaingeithiriaung": "你的chat_id"
}

def send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

    print(response.status_code)
    print(response.text)

@app.route("/trello-webhook", methods=["HEAD", "POST"])
def webhook():
    if request.method == "HEAD":
        return "", 200

    data = request.json
    print(data)

    action = data.get("action", {})
    action_type = action.get("type")

    if action_type == "addMemberToCard":
        member = action["member"]["username"]
        card_name = action["data"]["card"]["name"]

        chat_id = USER_MAP.get(member)

        if chat_id:
            send_telegram(
                chat_id,
                f"📌 新任务已分配：{card_name}"
            )

    return "OK", 200


if __name__ == "__main__":
    app.run(port=5000)