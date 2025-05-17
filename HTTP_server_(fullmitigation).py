from flask import Flask, request, jsonify, make_response
import subprocess
import time

app = Flask(__name__)

MAX_ATTEMPTS = 5        # Max allowed requests before ban
BAN_DURATION = 300      # Ban duration in seconds (5 minutes)

ip_attempts = {}
banned_ips = {}

def drop_ip(ip):
    """Run iptables command to block the IP at OS level."""
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"[!] IP {ip} has been dropped via iptables.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to drop IP {ip}: {e}")

@app.before_request
def check_and_ban_ip():
    ip = request.remote_addr

    # If already banned
    if ip in banned_ips:
        ban_time = banned_ips[ip]
        if time.time() - ban_time > BAN_DURATION:
            # Unban after timeout (optional: remove iptables rule manually if you want)
            del banned_ips[ip]
            ip_attempts[ip] = 0
        else:
            # Force close connection
            response = make_response("Your IP is temporarily banned.", 403)
            response.headers["Connection"] = "close"
            return response

    # Otherwise, count attempts
    ip_attempts[ip] = ip_attempts.get(ip, 0) + 1

    if ip_attempts[ip] > MAX_ATTEMPTS:
        banned_ips[ip] = time.time()
        del ip_attempts[ip]
        drop_ip(ip)  #Drop IP via iptables immediately
        response = make_response("Too many attempts. You are banned.", 403)
        response.headers["Connection"] = "close"
        return response

@app.route('/store', methods=['POST'])
def store_data():
    data = request.get_json()
    if data:
        return "Data received", 201
    return "Invalid or missing JSON", 400

if __name__ == "__main__":
    print("Server running on http://192.168.1.20:5000")
    app.run(debug=True, host="192.168.1.20", port=5000, use_reloader=False)

