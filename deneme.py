filename = "asd2.vtt"
import webvtt

start = []
end = []
text = []
speaker = []

for caption in webvtt.read(filename):
    start.append(caption.start)
    end.append(caption.end)
    text.append(caption.text)
    speaker.append(caption.raw_text)
          
with open(filename) as f:
    text = f.read()
 
print(text)

