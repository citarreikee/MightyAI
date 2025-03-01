from config import HOME_ASSISTANT_TOKEN
from yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light
import datetime

def adjust_light_settings(lamp):
    # 获取当前时间
    current_hour = datetime.datetime.now().hour
    
    if 6 <= current_hour < 18:  # 白天（早上6点到晚上6点）
        brightness = 100  # 亮度设置为60%
        color_temperature = 5000  # 色温设置为5000K
    else:  # 夜间（晚上6点到早上6点）
        brightness = 40  # 亮度设置为40%
        color_temperature = 3000  # 色温设置为3000K
    
    lamp.set_light_brightness(brightness)
    lamp.set_light_color_temperature(color_temperature)

if __name__ == "__main__":
    import datetime
    lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)
    
    # 调整灯光设置
    adjust_light_settings(lamp)