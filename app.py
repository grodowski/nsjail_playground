from flask import Flask, request, jsonify
import subprocess
import os
from uuid import uuid4

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_nsjail():
    data = request.get_json()
    python_script = data.get("script", "")

    if not python_script:
        return jsonify({"error": "No script provided"}), 400

    # TODO: validate incoming script
    # does it have a main fn
    # max length

    session_id = uuid4()
    script_path = f"/app/tmp_script_{session_id}.py"
    with open(script_path, "w") as script_file:
        script_file.write(python_script)

    print(f"running:\n{python_script}")

    nsjail_command = [
        "nsjail",
        "--config", "sandbox.cfg",
        "--", "/usr/local/bin/python3", "-Su", script_path
    ]

    try:
        result = subprocess.run(nsjail_command, check=True, capture_output=True, text=True)
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": str(e),
            "stdout": e.stdout,
            "stderr": e.stderr,
        })
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == '__main__':
    os.makedirs("/app", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port='8080')
