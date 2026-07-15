import os
import asyncio
from flask import Flask, request, jsonify
import edge_tts
import yt_dlp

app = Flask(__name__)

# Функция для скачивания геймплея
def download_gameplay(game_name):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'gameplay.mp4',
        'max_downloads': 1,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{game_name} gameplay 4k 60fps no commentary"])
    return "gameplay.mp4"

@app.route('/make_video', methods=['POST'])
def make_video():
    data = request.json
    script = data.get("script_text")
    game_name = data.get("game_name")
    
    # 1. Озвучка
    audio_file = "speech.mp3"
    asyncio.run(edge_tts.Communicate(script, "ru-RU-DmitryNeural").save(audio_file))
    
    # 2. Скачивание геймплея
    video_file = download_gameplay(game_name)
    
    return jsonify({"status": "Озвучка и геймплей готовы!", "files": [audio_file, video_file]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
