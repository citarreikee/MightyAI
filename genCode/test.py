from config import HOME_ASSISTANT_TOKEN
from yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light
import datetime
import time

lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)

def main():

    try:
        # 执行三长亮
        for _ in range(3):
            print("Long light on...")
            lamp.set_light_brightness(100)
            time.sleep(5)  # 保持3秒
            print("Long light off...")
            lamp.set_light_brightness(1)
            time.sleep(2)  # 短暂关闭

        # 执行三短闪
        for _ in range(3):
            print("Short flash on...")
            lamp.set_light_brightness(100)
            time.sleep(2)  # 保持0.5秒
            print("Short flash off...")
            lamp.set_light_brightness(1)
            time.sleep(2)

        # 执行三长亮
        for _ in range(3):
            print("Long light on...")
            lamp.set_light_brightness(100)
            time.sleep(5)  # 保持3秒
            print("Long light off...")
            lamp.set_light_brightness(1)
            time.sleep(2)  # 短暂关闭

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("sos light signal done.")

if __name__ == "__main__":

    main()