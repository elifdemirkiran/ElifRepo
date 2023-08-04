import datetime
import whisper
import webvtt

model = whisper.load_model('base.en')
option = whisper.DecodingOptions(language='en', fp16=False)
result = model.transcribe('HTML5 video accessibility and the WebVTT file format.mp4')

# print(result.keys())
# print(result['text'])s

save_target = 'video.vtt'

with open(save_target, 'w') as file:
    # Add a title to the WebVTT file
    file.write("WEBVTT - 2014 Three Minute Thesis winning presentation by Emily Johnston\n\n")
    for index, segment in enumerate(result['segments']):
        # Remove leading and trailing whitespaces
        text = segment['text'].strip()
        # Replace multiple whitespaces with a single space
        text = " ".join(text.split())
        file.write(str(index + 1) + '\n')
        file.write(str(datetime.timedelta(seconds=segment['start'])) + ' --> ' + str(
            datetime.timedelta(seconds=segment['end'])) + '\n')
        file.write(text + '\n')
        file.write('\n')
