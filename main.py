import os
import threading
from flask import Flask, request, jsonify
import edge_tts
import yt_dlp
# В версии 2.0+ импортируем напрямую из moviepy
from moviepy import VideoFileClip, AudioFileClip

app = Flask(__name__)

def process_video(script, game_name):
    try:
        print("Начинаю процесс обработки...")
        
        # 1. Озвучка
        audio_file = "speech.mp3"
        import asyncio
        asyncio.run(edge_tts.Communicate(script, "ru-RU-DmitryNeural").save(audio_file))
        
        # 2. Скачивание (без комментариев, лучшее качество)
        ydl_opts = {
            'format': 'best[ext=mp4]', 
            'outtmpl': 'gameplay.mp4', 
            'quiet': True,
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{game_name} gameplay 4k 60fps no commentary"])
            
        # 3. Монтаж
        video = VideoFileClip("gameplay.mp4")
        audio = AudioFileClip(audio_file)
        
        # Обрезаем видео под длину аудио
        duration = min(audio.duration, video.duration)
        final_video = video.with_audio(audio).subclipped(0, duration)
        
        # Сохранение
        final_video.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
        print("Монтаж успешно завершен!")
        
    except Exception as e:
        print(f"Ошибка в процессе обработки: {e}")

@app.route('/make_video', methods=['POST'])
def make_video():
    data = request.json
    script = data.get("script_text")
    game_name = data.get("game_name")
    
    if not script or not game_name:
        return jsonify({"status": "Ошибка: нет данных"}), 400
    
    # Запуск в фоне
    threading.Thread(target=process_video, args=(script, game_name)).start()
    
    return jsonify({"status": "Монтаж запущен в фоне!"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
