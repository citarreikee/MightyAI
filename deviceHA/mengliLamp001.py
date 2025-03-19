import asyncio
from bleak import BleakClient, BleakScanner

class MengliLamp001:
    def __init__(self, DEVICE_ADDRESS, CHARACTERISTIC_UUID_W, CHARACTERISTIC_UUID_R):
        self.MacAddress = DEVICE_ADDRESS
        self.UUID_W = CHARACTERISTIC_UUID_W
        self.UUID_R = CHARACTERISTIC_UUID_R

        # device = await BleakScanner.find_device_by_address(self.MacAddress)
        # if not device:
        #     print("设备未找到")
        # else:
        #     self.device = device
        
        
    async def set_light_brightness_up(self, brightness):
        data = [0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        # data[2] = f"0x{round(brightness * 2.5):02X}"
        data[2] = round(brightness * 2.5)
        data_to_send = bytes(data)
        async with BleakClient(self.MacAddress) as client:
            print(f"已连接: {client.is_connected}")
            await client.write_gatt_char(self.UUID_W, data_to_send)

if __name__ == "__main__":
    try:
        lamp = MengliLamp001("20:43:A8:6B:1D:2E","12a59e0a-17cc-11ec-9621-0242ac130002","12a5a148-17cc-11ec-9621-0242ac130002")
        asyncio.run(lamp.set_light_brightness_up(100)) 


    except KeyboardInterrupt:
        print("程序终止")
