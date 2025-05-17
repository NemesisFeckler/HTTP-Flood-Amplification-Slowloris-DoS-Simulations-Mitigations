from flask import Flask, request, jsonify
                

app = Flask(__name__)

# In-memory storage for uploaded JSON data
json_storage = []
ip_conncet = []


@app.route('/store', methods=['POST'])

def store_json():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    print("Received JSON:",data)

    filename = data.get("filename", f"file_{len(json_storage)}.json")

    json_entry = {
        "filename": filename,
        "content": data
        }

    json_storage.append(json_entry)
    return jsonify({"message": f"JSON '{filename}' stored successfully"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    filenames = [entry['filename'] for entry in json_storage]
    return jsonify({"stored_json_files": filenames}), 200

if __name__=='__main__':
    app.run(debug = True, host='192.168.1.20', port=5000)
