import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)  # 语速
engine.setProperty("volume", 0.9)  # 音量

text = "你好，这是一个本地TTS示例。"
engine.say(text)
engine.runAndWait()