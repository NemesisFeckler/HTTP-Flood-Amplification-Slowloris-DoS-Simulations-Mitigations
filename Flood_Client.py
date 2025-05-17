import requests, threading, os, json, time
from generate_monster_json import generate_monsters

# Generate monster JSON files
generate_monsters(5)

# Target server IP and port (replace with Ubuntu VM's IP)
URL = "http://192.168.1.20:5000/store"

# Load all generated JSON files
json_files = [os.path.join("generated", f) for f in os.listdir("generated") if f.endswith(".json")]

def send_file(file_path):
    with open(file_path, 'rb') as f:
        payload = json.load(f)
    while True:
        try:
            response = requests.post(URL, json=payload)
            print(f"[{file_path}] Status: {response.status_code}")
        except Exception as e:
            print(f"[{file_path}] Error: {e}")
        time.sleep(0.1)  # optional throttle

# Launch 5 threads per file
THREADS_PER_FILE = 15

for file_path in json_files:
    for _ in range(THREADS_PER_FILE):
        threading.Thread(target=send_file, args=(file_path,)).start()

