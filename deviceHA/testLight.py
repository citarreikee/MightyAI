# from deviceHA.config import HOME_ASSISTANT_TOKEN
# from deviceHA.yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light

from config import DEVICE_ADDRESS, CHARACTERISTIC_UUID_R, CHARACTERISTIC_UUID_W
from nani import MengliLamp001
from bleak import BleakClient, BleakScanner
import asyncio

# lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)

async def _send_command():
        data_to_send = []
        data = [0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        for i in range(100):
              data[2] = round(i * 2.5)
              data_to_send.append(bytes(data))
        
              
        async with BleakClient(DEVICE_ADDRESS) as client:
            for i in range(len(data_to_send)):
                await client.write_gatt_char(CHARACTERISTIC_UUID_W, data_to_send[i])
                print(f"亮度已设定{i}次")
            
        return "命令已发送"

asyncio.run(_send_command())

# lamp = MengliLamp001(DEVICE_ADDRESS,CHARACTERISTIC_UUID_R,CHARACTERISTIC_UUID_W)

    

# res = lamp.toggle() 
# print(res)