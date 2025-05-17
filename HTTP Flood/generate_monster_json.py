import json, random, string, os

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_nested_dict(depth, width):
    if depth == 0:
        return random_string(1000)
    return {f"key_{i}": generate_nested_dict(depth - 1, width) for i in range(width)}

def generate_json_payload():
    return {
        "metadata": {
            "id": random.randint(1, 999999),
            "name": random_string(100),
            "tags": [random_string(10) for _ in range(100)],
        },
        "payload": generate_nested_dict(8, 3),
        "array_of_objects": [{"index": i, "data": random_string(1000)} for i in range(100)],
        "crazy_numbers": [random.uniform(1e10, 1e20) for _ in range(500)],
        "massive_text": random_string(100000),
    }

def generate_monsters(n=5):
    os.makedirs("generated", exist_ok=True)
    for i in range(n):
        filename = f"generated/monster_{i+1}.json"
        with open(filename, "w") as f:
            json.dump(generate_json_payload(), f)
        print(f"✅ Generated: {filename}")

if __name__ == "__main__":
    generate_monsters(5)
