import os
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)
COUNT_FILE = Path("count.txt")
APP_PORT = int(os.environ.get("APP_PORT", "5556"))


def next_counter_value():
    if not COUNT_FILE.exists():
        COUNT_FILE.write_text("0", encoding="utf-8")

    counter = int(COUNT_FILE.read_text(encoding="utf-8").strip() or "0") + 1
    COUNT_FILE.write_text(str(counter), encoding="utf-8")
    return counter


@app.route('/api/hello', methods=['GET'])
def hello_spencer():
    counter = next_counter_value()

    return jsonify({
        "message": "Hello wimmer",
        "counter" : counter,
        "status": "success"
    })


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=APP_PORT)
