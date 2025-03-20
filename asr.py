from vosk import Model, KaldiRecognizer
import pyaudio
import json

model = Model("vosk-model-small-cn-0.22")  # 替换模型路径
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

print("开始录音，按Ctrl+C停止...")
try:
    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print("识别结果:", json.loads(result)["text"])
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()