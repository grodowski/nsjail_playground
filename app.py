from flask import Flask, request, jsonify
import subprocess
import os
from uuid import uuid4

app = Flask(__name__)


def generate_random_letter_string(length=12):
    uuid_str = uuid4().hex
    hex_to_alpha = {
        '0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e', '5': 'f',
        '6': 'g', '7': 'h', '8': 'i', '9': 'j', 'a': 'k', 'b': 'l',
        'c': 'm', 'd': 'n', 'e': 'o', 'f': 'p'
    }
    letter_string = ''.join(hex_to_alpha[char] for char in uuid_str)
    return letter_string[:length]


@app.route('/execute', methods=['POST'])
def run_nsjail():
    data = request.get_json()
    python_script = data.get("script", "")

    if not python_script:
        return jsonify({"error": "No script provided"}), 400

    session_id = generate_random_letter_string()
    script_path = f"/app/tmp_script_{session_id}.py"
    with open(script_path, "w") as script_file:
        script_file.write("import os; import time; import numpy; import pandas;\n")
        script_file.write(python_script)

    print(f"running:\n{python_script}")

    module_name = script_path.split("/")[-1].split(".")[0]
    nsjail_command = [
        "nsjail",
        "--config", "sandbox.cfg",
        "--", "/usr/local/bin/python3", "-c", f"from {module_name} import main; main()"
    ]

    try:
        result = subprocess.run(nsjail_command, check=True, capture_output=True, text=True)
        return jsonify({"stdout": result.stdout})
    except subprocess.CalledProcessError as e:
        if "cannot import name 'main'" in e.stderr:
            return jsonify({"error": "main function not found in the script"}), 400
        if "object is not callable" in e.stderr:
            return jsonify({"error": "main is not a function"}), 400

        return jsonify({
            "error": str(e),
            "stdout": e.stdout,
            "stderr": e.stderr,
        }), 400
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == '__main__':
    os.makedirs("/app", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port='8080')
