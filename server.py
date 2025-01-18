import http.server
import socketserver

# Configuración
HOST = "127.0.0.10"  # Cambia a la dirección IP deseada
PORT = 8080  # Puerto para el servidor

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Maneja las peticiones GET."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Servidor HTTP funcionando correctamente.")

def run_server():
    with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Servidor iniciado en {HOST}:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
