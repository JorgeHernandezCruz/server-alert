import requests
import time

# Configuración
SERVER_IP = "http://127.0.0.10:8080" 
CHECK_INTERVAL = 10  # Intervalo en segundos (1 minuto)

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
    while True:
        is_active = check_service(SERVER_IP)
        if is_active:
            print("Estado: Conectado.\n")
        else:
            print("Estado: No conectado.\n")
        
        print(f"Esperando {CHECK_INTERVAL} segundos para la próxima verificación...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

