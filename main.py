import os
import threading
from flask import Flask, request, jsonify
import edge_tts
import yt_dlp
from moviepy.editor import VideoFileClip, AudioFileClip

app = Flask(__name__)

def process_video(script, game_name):
    try:
        print("Начинаю процесс...")
        # 1. Озвучка
        audio_file = "speech.mp3"
        import asyncio
        asyncio.run(edge_tts.Communicate(script, "ru-RU-DmitryNeural").save(audio_file))
        print("Озвучка готова.")
        
        # 2. Скачивание
        ydl_opts = {
            'format': 'best[ext=mp4]', 
            'outtmpl': 'gameplay.mp4', 
            'quiet': True,
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{game_name} gameplay 4k 60fps no commentary"])
        print("Видео скачано.")
            
        # 3. Монтаж
        video = VideoFileClip("gameplay.mp4")
        audio = AudioFileClip(audio_file)
        # Ограничиваем видео по длине аудио
        final_video = video.set_audio(audio).subclip(0, min(audio.duration, video.duration))
        final_video.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
        print("Монтаж завершен!")
        
    except Exception as e:
        print(f"Критическая ошибка монтажа: {e}")

@app.route('/make_video', methods=['POST'])
def make_video():
    data = request.json
    script = data.get("script_text")
    game_name = data.get("game_name")
    
    if not script or not game_name:
        return jsonify({"status": "Ошибка: нет данных"}), 400
    
    # Запускаем в фоне, чтобы Flask не упал по таймауту
    threading.Thread(target=process_video, args=(script, game_name)).start()
    
    return jsonify({"status": "Монтаж запущен в фоне!"}), 200

@app.route('/', methods=['GET'])
def health_check():
    return "Server is running!", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
