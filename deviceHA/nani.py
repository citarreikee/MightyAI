import asyncio
from bleak import BleakClient, BleakScanner


class MengliLamp001:
    def __init__(self, DEVICE_ADDRESS, CHARACTERISTIC_UUID_W, CHARACTERISTIC_UUID_R):
        self.MacAddress = DEVICE_ADDRESS
        self.UUID_W = CHARACTERISTIC_UUID_W
        self.UUID_R = CHARACTERISTIC_UUID_R
        self.client = BleakClient(DEVICE_ADDRESS)
        self.connected = False
        self._response_event = asyncio.Event()
        self._response_data = None

    async def connect(self):
        """显式建立连接"""
        if not self.connected:
            await self.client.connect()
            self.connected = True
            # 连接后立即注册通知回调
            await self.client.start_notify(self.UUID_R, self._notification_handler)

    async def disconnect(self):
        """显式断开连接"""
        if self.connected:
            await self.client.stop_notify(self.UUID_R)
            await self.client.disconnect()
            self.connected = False

    def _notification_handler(self, sender, data):
        """ 蓝牙通知回调 """
        self._response_data = data
        self._response_event.set()

    async def _async_query(self, cmd_code, expect_resp_code, parser):
        """ 通用查询方法（适配持久化连接）"""
        # 确保连接已建立
        if not self.connected:
            await self.connect()

        # 发送查询命令
        send_data = bytes([cmd_code] + [0x00]*9)
        try:
            # 发送指令
            await self.client.write_gatt_char(self.UUID_W, send_data)
            
            # 等待响应（带超时）
            try:
                await asyncio.wait_for(self._response_event.wait(), timeout=3)
            except asyncio.TimeoutError:
                raise TimeoutError("设备响应超时")
            finally:
                self._response_event.clear()
            
            # 解析响应
            resp_bytes = list(self._response_data)
            if resp_bytes[0] != expect_resp_code:
                raise ValueError(f"响应命令码错误，期望0x{expect_resp_code:02X}，收到0x{resp_bytes[0]:02X}")
            
            return parser(resp_bytes)
        
        except Exception as e:
            # 发生异常时断开连接
            await self.disconnect()
            raise e

    async def _send_command(self, data):
        """ 发送命令方法（适配持久化连接）"""
        if not self.connected:
            await self.connect()
        
        try:
            await self.client.write_gatt_char(self.UUID_W, bytes(data))
            return "命令已发送"
        except Exception as e:
            await self.disconnect()
            raise e
        

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
    
    # 查询方法实现 ------------------------------
    async def get_sleep_status(self):
        """ 查询睡眠状态 
        Return: 'awake' 或 'asleep'
        """
        def parser(data):
            status = data[1]
            if status == 0x00: return "awake"
            elif status == 0x01: return "asleep"
            else: raise ValueError(f"无效状态值0x{status:02X}")
        
        return await self._async_query(0x21, 0x03, parser)

    async def get_human_presence(self):
        """ 查询人体存在 
        Return: bool 是否有人
        """
        def parser(data):
            status = data[1]
            if status == 0x00: return False
            elif status == 0x01: return True
            else: raise ValueError(f"无效存在值0x{status:02X}")
        
        return await self._async_query(0x22, 0x04, parser)

    async def get_ambient_light(self):
        """ 查询环境光亮度 
        Return: int 0-5等级
        """
        def parser(data):
            level = data[1]
            if 0x00 <= level <= 0x05:
                return level
            raise ValueError(f"无效亮度等级0x{level:02X}")
        
        return await self._async_query(0x23, 0x05, parser)

    async def get_light_brightness(self, light_type):
        """ 查询指定灯光亮度
        :param light_type: 'up'/'middle'/'night'
        Return: int 0-250
        """
        cmd_map = {
            'up': (0x24, 0x06),
            'middle': (0x25, 0x07),
            'night': (0x26, 0x08)
        }
        cmd_code, expect_code = cmd_map[light_type]
        
        def parser(data):
            return data[1]  # 直接返回亮度值
        
        return await self._async_query(cmd_code, expect_code, parser)

    async def get_charging_status(self):
        """ 查询充电状态 
        Return: bool 是否在充电
        """
        def parser(data):
            status = data[1]
            if status == 0x00: return True
            elif status == 0x01: return False
            else: raise ValueError(f"无效充电状态0x{status:02X}")
        
        return await self._async_query(0x27, 0x09, parser)

    async def get_light_color_temp(self, light_type):
        """ 查询灯光色温 
        :param light_type: 'up'/'middle'/'night'
        Return: int 2000-6000K
        """
        cmd_map = {
            'up': (0x28, 0x04),
            'middle': (0x29, 0x08),
            'night': (0x2A, 0x0C)
        }
        cmd_code, expect_code = cmd_map[light_type]
        
        def parser(data):
            # 组合高低字节（示例数据格式：[0x28, 高位, 低位]
            high = data[1]
            low = data[2]
            return (high << 8) | low
        
        return await self._async_query(cmd_code, expect_code, parser)

    async def get_motor_angle(self):
        """ 查询电机角度 
        Return: tuple (角度0-70, 方向'forward'/'backward')
        """
        def parser(data):
            angle = data[1]
            direction = data[2]
            if direction == 0x00: dir_str = "backward"
            elif direction == 0x01: dir_str = "forward"
            else: raise ValueError(f"无效方向值0x{direction:02X}")
            
            if not 0x00 <= angle <= 0x46:
                raise ValueError(f"无效角度值0x{angle:02X}")
            
            return (angle, dir_str)
        
        return await self._async_query(0x2B, 0x0D, parser)
    

async def main():
    lamp = MengliLamp001("20:43:A8:6B:1D:2E","12a59e0a-17cc-11ec-9621-0242ac130002","12a5a148-17cc-11ec-9621-0242ac130002")
    try:
        await lamp.connect()  # 显式建立连接
        
        # 混合使用查询和设置命令
        await lamp.set_normal_mode()
        print(await lamp.get_sleep_status())
        await lamp.set_motor_angle(0x01, 45)
        # 查询主灯色温
        temp = await lamp.get_light_color_temp('middle')
        print(f"主灯色温：{temp}K")  # 输出示例：主灯色温：4000K
        
    finally:
        await lamp.disconnect()  # 确保断开连接

asyncio.run(main())

    
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