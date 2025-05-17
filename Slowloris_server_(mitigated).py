import subprocess
from flask import Flask, request
from threading import Lock

app = Flask(__name__)

ip_connections = {}
banned_ips = set()
lock = Lock()

MAX_CONNECTIONS = 10

@app.before_request
def limit_connections():
    ip = request.remote_addr
    with lock:
        count = ip_connections.get(ip, 0)
        if count >= MAX_CONNECTIONS:
            if ip not in banned_ips:
                print(f"[!] Banning IP {ip} for exceeding {MAX_CONNECTIONS} connections.")
                subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
                banned_ips.add(ip)
            return "Too many connections", 429
        ip_connections[ip] = count + 1

@app.after_request
def release_connection(response):
    ip = request.remote_addr
    with lock:
        if ip in ip_connections:
            ip_connections[ip] -= 1
            if ip_connections[ip] <= 0:
                del ip_connections[ip]
    return response

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    return 'Upload received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
