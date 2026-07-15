from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/make_video', methods=['POST'])
def make_video():
    data = request.json
    print("Получены данные:", data)
    return jsonify({"status": "Принято!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
