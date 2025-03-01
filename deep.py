import json
import logging
import time
import requests
from datetime import datetime, timedelta

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class YeelinkLamp22Cad9Light:
    def __init__(self, token):
        self.set_miot_property_url = "http://127.0.0.1:8123/api/services/xiaomi_miot/set_miot_property"
        self.call_action_url = "http://127.0.0.1:8123/api/services/xiaomi_miot/call_action"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        self.entity_id = "light.yeelink_lamp22_cad9_light"

    def set_brightness(self, brightness):
        """设置亮度（1-100）"""
        payload = json.dumps({
            "entity_id": self.entity_id,
            "siid": 2,
            "piid": 2,
            "value": brightness
        })
        response = requests.post(self.set_miot_property_url, headers=self.headers, data=payload)
        if response.status_code == 200:
            logging.info(f"亮度已设置为 {brightness}")
        else:
            logging.error(f"设置亮度失败，状态码：{response.status_code}")

    def set_color_temperature(self, temperature):
        """设置色温（1-100）"""
        payload = json.dumps({
            "entity_id": self.entity_id,
            "siid": 2,
            "piid": 3,
            "value": temperature
        })
        response = requests.post(self.set_miot_property_url, headers=self.headers, data=payload)
        if response.status_code == 200:
            logging.info(f"色温已设置为 {temperature}")
        else:
            logging.error(f"设置色温失败，状态码：{response.status_code}")

    def toggle(self):
        """开关灯"""
        payload = json.dumps({
            "entity_id": self.entity_id,
            "siid": 2,
            "aiid": 1,
        })
        response = requests.post(self.call_action_url, headers=self.headers, data=payload)
        if response.status_code == 200:
            logging.info("灯已切换状态")
        else:
            logging.error(f"切换灯状态失败，状态码：{response.status_code}")

class LightAutomation:
    def __init__(self, token):
        self.token = token
        self.light = YeelinkLamp22Cad9Light(token)
        # 定义不同场景的亮度和色温
        self.scenes = {
            "morning": {"brightness": 80, "color_temp": 5500},    # 清晨：高亮、冷光
            "daytime": {"brightness": 60, "color_temp": 4500},     # 白天：适中亮度、自然光
            "evening": {"brightness": 40, "color_temp": 3200},     # 傍晚：低亮、暖光
            "night": {"brightness": 10, "color_temp": 2700}       # 晚上：低亮度、暖光
        }
    
    def set_scene(self, scene_name):
        """根据场景名称设置灯光"""
        if scene_name in self.scenes:
            brightness = self.scenes[scene_name]["brightness"]
            color_temp = self.scenes[scene_name]["color_temp"]
            logging.info(f"切换到 {scene_name} 场景：亮度={brightness}, 色温={color_temp}")
            self.light.set_brightness(brightness)
            self.light.set_color_temperature(color_temp)
        else:
            logging.error(f"场景 '{scene_name}' 不存在")

    def run_scheduler(self):
        """根据时间自动切换灯光模式"""
        while True:
            current_time = datetime.now().time()
            
            # 根据时间判断当前场景
            if 5 <= current_time.hour < 10:      # 清晨（5:00 - 9:59）
                self.set_scene("morning")
            elif 10 <= current_time.hour < 17:   # 白天（10:00 - 16:59）
                self.set_scene("daytime") 
            elif 17 <= current_time.hour < 21:   # 傍晚（17:00 - 20:59）
                self.set_scene("evening")
            else:                                # 晚上（21:00 - 4:59）
                self.set_scene("night")
            
            # 每隔一小时检查一次
            time.sleep(3600)

if __name__ == "__main__":
    # 替换为你的 Home Assistant token
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhOWNkYTIwNjZlYTY0OTRhODMzZjk4ZDkwNDc5NTMxOCIsImlhdCI6MTcyOTUyMjU0NywiZXhwIjoyMDQ0ODgyNTQ3fQ.yW-vWU2bkT-vUIiNvg6rnSPK4lXyjCSHd4LTJlQH6Xc"

    
    light_automation = LightAutomation(TOKEN)
    
    # 启动灯光自动化
    try:
        logging.info("启动灯光自动化...")
        light_automation.run_scheduler()
    except KeyboardInterrupt:
        logging.info("灯光自动化已停止")