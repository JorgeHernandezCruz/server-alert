import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración
SERVER_IP = "http://127.0.0.10:8080" 
CHECK_INTERVAL = 10  # Intervalo en segundos
MAX_FAILURES = 3  # Número máximo de intentos fallidos antes de enviar correo
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = "jorge.hernandezhtb@gmail.com"  
PASSWORD = "" #contraseña de aplicacion para gmail  
RECIPIENT_EMAIL = " "  #correo remitente

def send_email(ip):
    """Función para enviar un correo cuando el servicio no está disponible."""
    print(f"Enviando correo de alerta para {ip}...")
    try:
        subject = f"Alerta: Servicio inactivo en {ip}"
        body = f"El servicio en la dirección IP {ip} no está respondiendo correctamente después de {MAX_FAILURES} intentos."
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Conexión y envío del correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Establece una conexión segura
            server.login(EMAIL, PASSWORD)  # Inicia sesión con tus credenciales
            server.sendmail(EMAIL, RECIPIENT_EMAIL, msg.as_string())
            print(f"Correo enviado a {RECIPIENT_EMAIL}.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def check_service(ip):
    """Función para verificar el estado del servicio."""
    print(f"Verificando servicio en {ip}...")
    try:
        response = requests.get(ip, timeout=10)  # Tiempo máximo de espera 10s
        if response.status_code == 200:
            print(f"El servidor en {ip} está conectado. Código de estado: 200.")
            return True
        else:
            print(f"El servidor en {ip} devolvió un código de estado: {response.status_code}.")
            return False
    except requests.RequestException as e:
        print(f"Error al conectar con {ip}: {e}")
        return False

def main():
    print("Iniciando script de validación del servidor...\n")
    consecutive_failures = 0

    while True:
        is_active = check_service(SERVER_IP)
        if is_active:
            print("Estado: Conectado.\n")
            consecutive_failures = 0  # Resetear contador si el servidor está activo
        else:
            print("Estado: No conectado.\n")
            consecutive_failures += 1

            if consecutive_failures >= MAX_FAILURES:
                print(f"El servidor ha fallado {MAX_FAILURES} veces consecutivas.")
                send_email(SERVER_IP)
                consecutive_failures = 0  # Resetear contador después de enviar correo
        
        print(f"Esperando {CHECK_INTERVAL} segundos para la próxima verificación...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
    #se termina
