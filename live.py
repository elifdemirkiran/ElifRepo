import os
import shutil
import tempfile
from urllib.parse import urljoin
from datetime import datetime, timedelta
import time
import m3u8
import requests
from pydub import AudioSegment
import speech_recognition as sr

base_url = 'https://dogus-live.daioncdn.net/startv/'
playlist_url = 'https://dogus-live.daioncdn.net/startv/startv_360p.m3u8'

recognizer = sr.Recognizer()

playlist_response = requests.get(playlist_url)
playlist = m3u8.loads(playlist_response.text)

start_time = datetime.now()

for i, segment in enumerate(playlist.segments):
    segment_url = urljoin(base_url, segment.uri)
    response = requests.get(segment_url, stream=True)
    response.raise_for_status()

    temp_dir = tempfile.mkdtemp()
    temp_ts_file = os.path.join(temp_dir, 'temp.ts')
    temp_wav_file = os.path.join(temp_dir, 'temp.wav')

    with open(temp_ts_file, 'wb') as f:
        f.write(response.raw.read())

    audio = AudioSegment.from_file(temp_ts_file, format='mpegts')
    audio.export(temp_wav_file, format='wav')

    with sr.AudioFile(temp_wav_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='tr-TR')
            duration = segment.duration
            start = start_time + timedelta(seconds=i * duration)
            end = start_time + timedelta(seconds=(i + 1) * duration)
            print(f"[{start:%H:%M:%S}-{end:%H:%M:%S}] {text}")
        except sr.UnknownValueError:
            print(f"[{start:%H:%M:%S}-{end:%H:%M:%S}] Ses dosyası anlaşılamadı.")
        except sr.RequestError as e:
            print(f"[{start:%H:%M:%S}-{end:%H:%M:%S}] Hata: {e}")

    os.remove(temp_ts_file)
    os.remove(temp_wav_file)
    shutil.rmtree(temp_dir)

    time_diff = (datetime.now() - start_time).total_seconds()
    sleep_time = max(0, segment.duration - time_diff)
    time.sleep(sleep_time)