import whisper
import pyaudio
import numpy as np
import threading

model = whisper.load_model("small")

# 录音参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024  # 每次读取的音频块大小

audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# 录音缓存
audio_buffer = []

def transcribe_audio():
    global audio_buffer
    while True:
        if len(audio_buffer) * CHUNK > RATE * 5:  # 每 5 秒识别一次
            audio_np = np.frombuffer(b''.join(audio_buffer), dtype=np.int16)
            audio_np = audio_np.astype(np.float32) / 32768.0  # 转换为浮点数
            result = model.transcribe(audio_np)
            print("实时结果:", result["text"])
            audio_buffer = []

# 启动识别线程
thread = threading.Thread(target=transcribe_audio)
thread.daemon = True
thread.start()

print("开始录音，按 Enter 键停止...")
try:
    while True:
        data = stream.read(CHUNK)
        audio_buffer.append(data)
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    audio.terminate()
