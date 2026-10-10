import os
import glob
import http.server
import socketserver
import webbrowser

PORT = 8000

class AutoHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin-allow-popups')
        super().end_headers()

    def do_GET(self):
        # Se o usuário acessar a raiz (/), encontra automaticamente o arquivo HTML da pasta
        if self.path == "/" or self.path == "":
            html_files = [f for f in os.listdir(".") if f.lower().endswith(".html")]
            if html_files:
                # Prioriza index.html ou prototipo_app_escrita
                target = "index.html" if "index.html" in html_files else html_files[0]
                self.send_response(302)
                self.send_header("Location", f"/{target}")
                self.end_headers()
                return
        return super().do_GET()

if __name__ == "__main__":
    current_dir = os.path.abspath(".")
    files = os.listdir(current_dir)
    html_files = [f for f in files if f.lower().endswith(".html")]

    print("=" * 60)
    print("📁 Pasta atual do servidor:", current_dir)
    print("📄 Arquivos encontrados na pasta:", files)
    if html_files:
        print("✓ Arquivo HTML detectado:", html_files[0])
    else:
        print("⚠️ ATENÇÃO: Nenhum arquivo .html encontrado nesta pasta!")
    print("=" * 60)
    print(f"🚀 Acesse no seu navegador: http://localhost:{PORT}")
    print("=" * 60)

    with socketserver.TCPServer(("", PORT), AutoHandler) as httpd:
        try:
            target_url = f"http://localhost:{PORT}/{html_files[0]}" if html_files else f"http://localhost:{PORT}"
            webbrowser.open(target_url)
        except Exception:
            pass
        httpd.serve_forever()
