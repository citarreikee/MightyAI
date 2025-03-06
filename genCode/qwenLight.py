from deviceHA.config import HOME_ASSISTANT_TOKEN
from deviceHA.yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light
import datetime
import time

# 初始化灯具控制对象
lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)

scenes = {
    "morning": {"time_range": (5, 10), "brightness": 70, "color_temperature": 5000},
    "day": {"time_range": (10, 18), "brightness": 60, "color_temperature": 4000},
    "evening": {"time_range": (18, 22), "brightness": 100, "color_temperature": 3000},
    "bedtime": {"time_range": (22, 5), "brightness": 1, "color_temperature": 2700}
}

def get_current_scene():
    current_hour = datetime.datetime.now().hour
    for scene, settings in scenes.items():
        start_hour, end_hour = settings["time_range"]
        if start_hour <= end_hour:
            if start_hour <= current_hour < end_hour:
                return scene
        else:  # 跨越午夜，比如 bedtime from 22 to 5
            if current_hour >= start_hour or current_hour < end_hour:
                return scene
    return None

def set_scene(scene_name):
    if scene_name in scenes:
        settings = scenes[scene_name]
        lamp.set_light_brightness(settings["brightness"])
        lamp.set_light_color_temperature(settings["color_temperature"])
        print(f"Scene '{scene_name}' set.")
    else:
        print("Invalid scene name.")

def main():
    while True:
        current_scene = get_current_scene()
        if current_scene:
            set_scene(current_scene)
        else:
            print("No scene matched the current time.")
        
        # 可以添加一个延迟，比如每小时检查一次
        time.sleep(3600)

if __name__ == "__main__":
    main()