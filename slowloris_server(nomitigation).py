import socket
import threading

HOST = '0.0.0.0'
PORT = 80
MAX_CONNECTIONS = 1024  # Accept up to this many clients

def handle_client(client_socket, addr):
    print(f"[+] Connected from {addr}")
    try:
        # Read data VERY slowly / indefinitely
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[{addr}] Received: {data.decode(errors='ignore').strip()}")
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Disconnected {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)
    print(f"[+] Listening on {HOST}:{PORT}...")

    try:
        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
        server.close()

if __name__ == "__main__":
    main()

