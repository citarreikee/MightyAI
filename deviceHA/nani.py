import asyncio
from bleak import BleakClient, BleakScanner


class MengliLamp001:
    def __init__(self, DEVICE_ADDRESS, CHARACTERISTIC_UUID_W, CHARACTERISTIC_UUID_R):
        self.MacAddress = DEVICE_ADDRESS
        self.UUID_W = CHARACTERISTIC_UUID_W
        self.UUID_R = CHARACTERISTIC_UUID_R
        self.client = BleakClient(DEVICE_ADDRESS)  # 持久化连接对象
        self.connected = False

    async def connect(self):
        """显式建立连接"""
        if not self.connected:
            await self.client.connect()
            self.connected = True

    async def disconnect(self):
        """显式断开连接"""
        if self.connected:
            await self.client.disconnect()
            self.connected = False

    def _brightness_to_hex(self, brightness):
        return round(brightness * 2.5)

    def _split_temp(self, temp):
        if not 2000 <= temp <= 6000:
            raise ValueError("色温值必须在2000到6000之间")
        hex_bytes = temp.to_bytes(2, byteorder='big')
        return [hex_bytes[0], hex_bytes[1]]

    async def _send_command(self, data):
        
        """复用已建立的连接"""
        if not self.client.is_connected:
            await self.connect()

        try:
            await self.client.write_gatt_char(
                self.UUID_W, 
                bytes(data),
            )
        
        except Exception as e:
            self.connected = False
            raise e
        return "命令已发送"
        # data_to_send = bytes(data)
        # async with BleakClient(self.MacAddress) as client:
        #     await client.write_gatt_char(self.UUID_W, data_to_send)
        

    # 亮度控制 ------------------------------
    async def set_light_brightness_up(self, brightness):
        data = [0x33] + [0x00]*9
        data[1] = self._brightness_to_hex(brightness)
        return await self._send_command(data)

    async def set_light_brightness_middle(self, brightness):
        data = [0x34] + [0x00]*9
        data[2] = self._brightness_to_hex(brightness)
        return await self._send_command(data)

    async def set_light_brightness_night(self, brightness):
        data = [0x35] + [0x00]*9
        data[3] = self._brightness_to_hex(brightness)
        return await self._send_command(data)

    async def set_light_brightness_up_middle(self, up, middle):
        data = [0x36] + [0x00]*9
        data[1] = self._brightness_to_hex(up)
        data[2] = self._brightness_to_hex(middle)
        return await self._send_command(data)

    async def set_light_brightness_middle_night(self, middle, night):
        data = [0x37] + [0x00]*9
        data[2] = self._brightness_to_hex(middle)
        data[3] = self._brightness_to_hex(night)
        return await self._send_command(data)

    async def set_light_brightness_up_night(self, up, night):
        data = [0x38] + [0x00]*9
        data[1] = self._brightness_to_hex(up)
        data[3] = self._brightness_to_hex(night)
        return await self._send_command(data)

    async def set_all_light_brightness(self, up, middle, night):
        data = [0x39] + [0x00]*9
        data[1] = self._brightness_to_hex(up)
        data[2] = self._brightness_to_hex(middle)
        data[3] = self._brightness_to_hex(night)
        return await self._send_command(data)

    # 色温控制 ------------------------------
    async def set_light_color_temp_up(self, temp):
        data = [0x3D] + [0x00]*9
        data[4:6] = self._split_temp(temp)
        return await self._send_command(data)

    async def set_light_color_temp_middle(self, temp):
        data = [0x3E] + [0x00]*9
        data[6:8] = self._split_temp(temp)
        return await self._send_command(data)

    async def set_light_color_temp_night(self, temp):
        data = [0x3F] + [0x00]*9
        data[8:10] = self._split_temp(temp)
        return await self._send_command(data)

    async def set_light_color_temp_up_middle(self, up_temp, middle_temp):
        data = [0x40] + [0x00]*9
        data[4:6] = self._split_temp(up_temp)
        data[6:8] = self._split_temp(middle_temp)
        return await self._send_command(data)

    async def set_light_color_temp_middle_night(self, middle_temp, night_temp):
        data = [0x41] + [0x00]*9
        data[6:8] = self._split_temp(middle_temp)
        data[8:10] = self._split_temp(night_temp)
        return await self._send_command(data)

    async def set_light_color_temp_up_night(self, up_temp, night_temp):
        data = [0x42] + [0x00]*9
        data[4:6] = self._split_temp(up_temp)
        data[8:10] = self._split_temp(night_temp)
        return await self._send_command(data)

    async def set_all_light_color_temp(self, up, middle, night):
        data = [0x43] + [0x00]*9
        data[4:6] = self._split_temp(up)
        data[6:8] = self._split_temp(middle)
        data[8:10] = self._split_temp(night)
        return await self._send_command(data)

    # 电机控制 ------------------------------
    async def set_motor_angle(self, direction, angle):
        if direction not in (0x00, 0x01):
            raise ValueError("方向参数错误，0x00: 反向, 0x01: 正向")
        if not 0 <= angle <= 70:
            raise ValueError("角度范围0-70度")
        
        data = [0x07] + [0x00]*9
        data[1] = direction
        data[2] = angle
        return await self._send_command(data)

    # 闹钟设置 ------------------------------
    async def set_alarm(self, hours, minutes):
        data = [0x08] + [0x00]*9
        data[1] = hours
        data[2] = minutes
        return await self._send_command(data)

    async def cancel_alarm(self):
        data = [0x0A] + [0x00]*9
        return await self._send_command(data)

    # 模式切换 ------------------------------
    async def set_normal_mode(self):
        data = [0x64] + [0x00]*9
        return await self._send_command(data)

    async def set_reading_mode(self):
        data = [0x65] + [0x00]*9
        return await self._send_command(data)

    async def set_sleep_mode(self):
        data = [0x66] + [0x00]*9
        return await self._send_command(data)
    
# if __name__ == "__main__":
#     try:
#         lamp = MengliLamp001("20:43:A8:6B:1D:2E","12a59e0a-17cc-11ec-9621-0242ac130002","12a5a148-17cc-11ec-9621-0242ac130002")
#         asyncio.run(lamp.set_all_light_color_temp(5800,5800,5800))
                    
#     except KeyboardInterrupt:
#         print("程序终止")

# import asyncio
# from math import pi, sin

# class LightShow:
#     def __init__(self, lamp):
#         self.lamp = lamp
        
#     async def breathe_effect(self, duration=10, cycles=3):
#         """呼吸灯效果：亮度正弦波动，色温同步渐变"""
#         for _ in range(cycles):
#             for i in range(101):
#                 # 使用正弦曲线生成更自然的呼吸效果
#                 brightness = 50 * (1 + sin(2 * pi * i / 100))  # 0~100范围波动
#                 temp = 2000 + int(4000 * i / 100)  # 色温从2000K到6000K
                
#                 # 同时设置所有灯光
#                 await self.lamp.set_all_light_brightness(brightness, brightness, brightness)
#                 print(f"亮度设定为：{brightness}")
#                 await self.lamp.set_all_light_color_temp(temp, temp, temp)
#                 print(f"色温设定为：{temp}")
#                 await asyncio.sleep(duration/100)
#                 print(f"休眠：{duration/100}")
                
#             for i in reversed(range(101)):
#                 brightness = 50 * (1 + sin(2 * pi * i / 100))
#                 temp = 6000 - int(4000 * i / 100)
                
#                 await self.lamp.set_all_light_brightness(brightness, brightness, brightness)
#                 print(f"亮度设定为：{brightness}")
#                 await self.lamp.set_all_light_color_temp(temp, temp, temp)
#                 print(f"色温设定为：{temp}")
#                 await asyncio.sleep(duration/100)
#                 print(f"休眠：{duration/100}")

#     async def sunrise_wakeup(self, duration=300):
#         """模拟日出效果：亮度从0到100%，色温从暖黄到自然白"""
#         steps = int(duration)
#         for i in range(steps):
#             progress = i / steps
#             brightness = 100 * progress
#             temp = 2000 + int(4000 * progress)
            
#             await self.lamp.set_all_light_brightness(brightness, brightness, brightness)
#             print(f"亮度设定为：{brightness}")
#             await self.lamp.set_all_light_color_temp(temp, temp, temp)
#             print(f"色温设定为：{temp}")
#             await asyncio.sleep(0.1)

# async def main():
#     # 设备信息需要替换为实际值
#     LAMP_ADDRESS = "20:43:A8:6B:1D:2E"
#     UUID_W = "12a59e0a-17cc-11ec-9621-0242ac130002"
#     UUID_R = "12a5a148-17cc-11ec-9621-0242ac130002"

#     lamp = MengliLamp001(LAMP_ADDRESS, UUID_W, UUID_R)
#     show = LightShow(lamp)

#     try:
#         print("启动呼吸灯效果...")
#         await show.breathe_effect(duration=8, cycles=2)
        
#         print("启动日出唤醒效果...")
#         await show.sunrise_wakeup(duration=20)
        
#     except Exception as e:
#         print(f"发生错误: {str(e)}")
#     finally:
#         # 重置为默认状态
#         await lamp.set_all_light_brightness(50, 50, 50)
#         await lamp.set_normal_mode()

# if __name__ == "__main__":
#     asyncio.run(main())