from config import HOME_ASSISTANT_TOKEN
from yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light

import keyboard

# lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)

# # 呼吸灯    
# i = 50
# direction = 1  # 1 表示递增，-1 表示递减

# while True:  # 无限循环
#     lamp.set_light_brightness(i)
        
#     if (i == 50 and direction == -1) or (i == 100 and direction == 1):
#         direction *= -1  # 改变方向
#     i += 50 * direction

# Add hotkey for Ctrl+J+K and call the check_hotkey function

# keyboard.add_hotkey('j',lamp.toggle)
# keyboard.wait('esc')

import time

class SOSSignalSender:
    def __init__(self, light):
        self.light = light
        self.is_running = True

    def send_sos_signal(self):
        # 摩尔斯电码中的SOS是...---...
        morse_code = {'S': '...', 'O': '---'}
        sos_sequence = [morse_code['S'], morse_code['O'], morse_code['S']]

        # 定义点和划的持续时间
        dot_duration = 0.5  # 点的持续时间，秒
        dash_duration = 1.5  # 划的持续时间，秒
        between_elements = 0.5  # 字母内元素之间的间隔，秒
        between_letters = 1.0  # 字母之间的间隔，秒
        between_words = 3.0  # 次之间的间隔，秒

        try:
            while self.is_running:
                for word in sos_sequence:
                    for letter in word:
                        if letter == '.':
                            self.light.toggle()  # 开灯
                            time.sleep(dot_duration)
                            self.light.toggle()  # 关灯
                            time.sleep(between_elements)
                        elif letter == '-':
                            self.light.toggle()  # 开灯
                            time.sleep(dash_duration)
                            self.light.toggle()  # 关灯
                            time.sleep(between_elements)
                    time.sleep(between_letters)  # 字母之间的时间间隔
                time.sleep(between_words)  # 单词之间的间隔

                # 检查是否需要停止
                if not self.is_running:
                    break

        except KeyboardInterrupt:
            pass
        finally:
            # 确保灯是关的
            self.light.toggle()

    def stop(self):
        self.is_running = False

def main():
    lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)
    sender = SOSSignalSender(lamp)

    print("准备发送SOS信号...")
    print("按 'q' 键停止发送。")

    # 使用键盘监听来停止发送
    keyboard.add_hotkey('q', lda: sender.stop())

    try:
        sender.send_sos_signal()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("SOS信号发送已完成。")

if __name__ == "__main__":
    main()







