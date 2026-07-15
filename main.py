import os
import threading
from flask import Flask, request, jsonify
import edge_tts
import yt_dlp
from moviepy.editor import VideoFileClip, AudioFileClip

app = Flask(__name__)

def process_video(script, game_name):
    try:
        # 1. Озвучка
        audio_file = "speech.mp3"
        # Для фонового потока используем синхронный подход или вызываем через loop
        import asyncio
        asyncio.run(edge_tts.Communicate(script, "ru-RU-DmitryNeural").save(audio_file))
        
        # 2. Скачивание
        ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'outtmpl': 'gameplay.mp4', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{game_name} gameplay 4k 60fps no commentary"])
            
        # 3. Монтаж
        video = VideoFileClip("gameplay.mp4")
        audio = AudioFileClip(audio_file)
        final_video = video.set_audio(audio).subclip(0, audio.duration)
        final_video.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
        print("Монтаж завершен!")
    except Exception as e:
        print(f"Ошибка: {e}")

@app.route('/make_video', methods=['POST'])
def make_video():
    data = request.json
    script = data.get("script_text")
    game_name = data.get("game_name")
    
    # Запускаем в отдельном потоке (background thread)
    threading.Thread(target=process_video, args=(script, game_name)).start()
    
    return jsonify({"status": "Монтаж запущен в фоне!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
