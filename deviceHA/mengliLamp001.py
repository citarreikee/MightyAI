import asyncio
from bleak import BleakClient, BleakScanner

class MengliLamp001:
    def __init__(self, DEVICE_ADDRESS, CHARACTERISTIC_UUID_W, CHARACTERISTIC_UUID_R):
        self.MacAddress = DEVICE_ADDRESS
        self.UUID_W = CHARACTERISTIC_UUID_W
        self.UUID_R = CHARACTERISTIC_UUID_R        
        
    async def set_light_brightness_up(self, brightness):
        data = [0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        
        data[1] = round(brightness * 2.5)
        data_to_send = bytes(data)
        async with BleakClient(self.MacAddress) as client:
            print(f"设备连接状态: {client.is_connected}")
            await client.write_gatt_char(self.UUID_W, data_to_send)
        return "命令已发送"


    async def set_light_brightness_middle(self, brightness):
        data = [0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        
        data[2] = round(brightness * 2.5)
        data_to_send = bytes(data)
        async with BleakClient(self.MacAddress) as client:
            print(f"设备连接状态: {client.is_connected}")
            await client.write_gatt_char(self.UUID_W, data_to_send)

        return "命令已发送"
 
