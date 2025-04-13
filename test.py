# def map_brightness(percentage):
#     # 限制输入范围在0-100
#     clamped = max(0, min(100, percentage))
#     # 线性映射到0-250并四舍五入
#     return round(clamped * 2.5)

# # 使用示例
# brightness = 50  # 输入0-100的亮度值
# hex_value = map_brightness(brightness)

# # 发送给灯控设备（示例）
# # ser.write(bytes([hex_value]))  # 假设使用串口通信
# print(f"发送的十六进制值: 0x{hex_value:02X}")
# print(hex(hex_value))
# print(f"{hex_value:02X}")

data_to_send = bytes([0x22, 2, 0x03, 4, 5, 6, 36, 8, 9, 17])

i = bytes(3)

print(data_to_send)
print(list(data_to_send))
print(i)
