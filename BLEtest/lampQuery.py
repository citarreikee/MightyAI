import asyncio
from bleak import BleakClient, BleakScanner

DEVICE_ADDRESS = "20:43:A8:6B:1D:2E"
CHARACTERISTIC_UUID_W = "12a59e0a-17cc-11ec-9621-0242ac130002"  # 写指令
CHARACTERISTIC_UUID_R = "12a5a148-17cc-11ec-9621-0242ac130002"  # 读通知

class BLEManager:
    def __init__(self):
        self.response_received = asyncio.Event()  # 异步事件
        self.response_data = None

    def notification_handler(self, sender: str, data: bytearray):
        """处理通知数据，验证是否为预期响应"""
        # # 示例：假设数据以 0x55 开头视为有效响应
        # if data.startswith(b'\x55'):
        #     self.response_data = data
        #     self.response_received.set()  # 触发事件
        print(f"接收数据: {data.hex()}")
        self.response_received.set()

    async def query_device(self, client, command: bytes, timeout=5) -> bytes:
        """发送指令并等待响应"""
        self.response_received.clear()
        self.response_data = None
        # 发送指令
        await client.write_gatt_char(CHARACTERISTIC_UUID_W, command, response=True)
        try:
            # 等待事件触发（最多等待 timeout 秒）
            await asyncio.wait_for(self.response_received.wait(), timeout)
            return self.response_data
        except asyncio.TimeoutError:
            print("等待响应超时")
            return None

async def main():
    manager = BLEManager()
    device = await BleakScanner.find_device_by_address(DEVICE_ADDRESS)
    if not device:
        print("设备未找到")
        return

    async with BleakClient(device) as client:
        print(f"已连接: {client.is_connected}")
        # 启用通知
        await client.start_notify(CHARACTERISTIC_UUID_R, manager.notification_handler)
        
        # 示例：发送查询指令 0x02 并等待响应
        data_to_send = bytes([0x34, 0x00, 0xF9, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        response = await manager.query_device(client, data_to_send)
        if response:
            print(f"收到响应: {response.hex()}")
        
        # 保持运行以接收其他通知
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序终止")