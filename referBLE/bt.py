import asyncio
from bleak import BleakClient, BleakScanner
import time

DEVICE_ADDRESS = "20:43:A8:6B:1D:2E"  # 替换为你的设备地址
CHARACTERISTIC_UUID = "12a59e0a-17cc-11ec-9621-0242ac130002"  # 替换为你的特征UUID

async def connect_with_retry(address, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            async with BleakClient(address, timeout=10.0) as client:
                # 显式等待服务发现完成
                await client.get_services()
                print("连接成功，服务已加载！")
                return client
        except Exception as e:
            print(f"连接失败（尝试 {retries+1}/{max_retries}）: {str(e)}")
            retries += 1
            await asyncio.sleep(1)
    raise Exception("无法连接设备")

async def control_device():
    try:
        client = await connect_with_retry(DEVICE_ADDRESS)
        data_to_send = bytes([0x34, 0x00, 0xF9, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        await client.write_gatt_char(CHARACTERISTIC_UUID, data_to_send, response=True)
        print("数据发送成功！")
        # 读取数据（可选）
        while True:
            data = await client.read_gatt_char("12a5a148-17cc-11ec-9621-0242ac130002")
            print(f"接收数据: {data.hex()}")
            time.sleep(1)
        
    except Exception as e:
        print(f"蓝牙操作失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(control_device())


