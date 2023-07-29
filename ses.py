import os
import shutil
import tempfile
from urllib.parse import urljoin

import m3u8
import requests
from pydub import AudioSegment
import speech_recognition as sr

base_url = 'https://dogus-live.daioncdn.net/startv/'
playlist_url = 'https://dogus-live.daioncdn.net/startv/startv_360p.m3u8'

playlist_response = requests.get(playlist_url)
playlist = m3u8.loads(playlist_response.text)
temp_dir = tempfile.mkdtemp()
temp_ts_file = os.path.join(temp_dir, 'temp.ts')
temp_wav_file = os.path.join(temp_dir, 'temp.wav')

recognizer = sr.Recognizer()

for segment in playlist.segments:
    segment_url = urljoin(base_url, segment.uri)
    response = requests.get(segment_url)
    
    with open(temp_ts_file, 'wb') as f:
        f.write(response.content)

    try:
        audio = AudioSegment.from_file(temp_ts_file, format='mpegts')
        audio.export(temp_wav_file, format='wav')

        with sr.AudioFile(temp_wav_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language='tr-TR')
                print(text)
            except sr.UnknownValueError:
                print('Ses dosyası anlaşılamadı.')
            except sr.RequestError as e:
                print(f'Hata: {e}')
    except Exception as e:
        print(f"İşlem sırasında bir hata oluştu: {e}")

    os.remove(temp_ts_file)

os.remove(temp_wav_file)
shutil.rmtree(temp_dir)