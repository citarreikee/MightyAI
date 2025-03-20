from . import config
from . import yeelinkLamp22Cad9Light
from . import nani
from . import wifiSpeaker

# 初始化灯具控制对象
# lamp = yeelinkLamp22Cad9Light.YeelinkLamp22Cad9Light(config.HOME_ASSISTANT_TOKEN)
lamp = nani.MengliLamp001(config.DEVICE_ADDRESS,config.CHARACTERISTIC_UUID_W,config.CHARACTERISTIC_UUID_R)
speaker = wifiSpeaker.WifiSpaekerlx06(config.HOME_ASSISTANT_TOKEN)

# from config import HOME_ASSISTANT_TOKEN
# from yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light

# lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)

