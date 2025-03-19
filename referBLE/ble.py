import asyncio
from bleak import BleakScanner, BleakClient

async def main():
    # 扫描设备
    print("开始扫描...")
    devices = await BleakScanner.discover()
    print(devices)
    target_device = None
    for device in devices:
        if device.address == "20:43:A8:6B:1D:2E":
            print("目标设备已经找到")
            target_device = device
            break
    if not target_device:
        print("设备未找到")
        return

    # 连接设备
    async with BleakClient(target_device.address, timeout=30) as client:
        
        if not await client.is_connected():
            print("连接失败")
            return
        
        print("连接成功！尝试获取服务...")
        try:
            # 手动触发服务发现
            services = await client.get_services()
            print(services)
            # for service in services:
            #     for char in service.characteristics:
            #         if char.uuid == "12a59e0a-17cc-11ec-9621-0242ac130002":
            #             print(f"特征属性: {char.properties}")  # 应包含 "write"
        except Exception as e:
            print(f"服务发现失败: {e}")
            return
        
        # 写入特征值
        data_to_send = bytes([0x34, 0x00, 0xF9, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        await client.write_gatt_char("12a59e0a-17cc-11ec-9621-0242ac130002", data_to_send)
        print("数据发送成功")
        

asyncio.run(main())


#20:43:A8:6B:1D:2E

# async def scan():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         if d.name == "小黑2":
#             print(f"确认地址: {d.address}")  # 检查输出是否与目标地址一致
# asyncio.run(scan())
