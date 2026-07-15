import os
import asyncio
from flask import Flask, request, jsonify
import edge_tts

app = Flask(__name__)

async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "ru-RU-DmitryNeural")
    await communicate.save(output_file)

@app.route('/make_video', methods=['POST'])
def make_video():
    data = request.json
    script = data.get("script_text")
    
    # Запускаем озвучку
    audio_file = "speech.mp3"
    asyncio.run(generate_audio(script, audio_file))
    
    return jsonify({"status": "Озвучка готова!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
