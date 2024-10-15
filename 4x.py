import psutil
import threading
import numpy as np
import time
import pystray
from PIL import Image, ImageDraw
import os
import sys

# 用于控制任务是否运行的标志
running = True

# 增加CPU负载
def cpu_heavy_task():
    while running:
        result = 0
        for i in range(1, 10000000):
            result += i ** 2

# 增加内存负载
def memory_heavy_task():
    memory_heavy_list = []
    while running:
        memory_heavy_list.append(np.random.rand(10000, 10000))
        if len(memory_heavy_list) > 100:
            memory_heavy_list = memory_heavy_list[10:]

# 检查是否指定程序在运行
def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

# 启动CPU和内存占用任务
def start_heavy_tasks():
    print("启动 CPU 和内存占用任务...")
    cpu_threads = []
    for _ in range(4):  # 可以根据 CPU 核心数调整
        thread = threading.Thread(target=cpu_heavy_task)
        cpu_threads.append(thread)
        thread.start()

    memory_thread = threading.Thread(target=memory_heavy_task)
    memory_thread.start()

    # 保持线程运行
    for thread in cpu_threads:
        thread.join()
    memory_thread.join()

# 创建系统托盘图标
def create_image(width, height, color1, color2):
    # 创建一个简单的图标
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

# 退出程序并停止占用
def on_quit(icon, item):
    global running
    running = False  # 停止占用任务
    icon.stop()  # 停止托盘图标
    sys.exit()  # 退出程序

# 托盘图标设置
def setup_tray_icon():
    icon = pystray.Icon("TestIcon")
    icon.icon = create_image(64, 64, "blue", "white")  # 自定义图标
    icon.menu = pystray.Menu(pystray.MenuItem("退出", on_quit))
    icon.run(setup_monitor)

# 监控指定程序是否运行
def setup_monitor(icon):
    print("开始监控程序...")
    while True:
        if is_process_running("DeltaForceClient-Win64-Shipping.exe"):  # 监控程序是否运行这里可以改需要的程序名
            print("检测到 DeltaForceClient-Win64-Shipping.exe 正在运行，启动占用任务...")
            start_heavy_tasks()
            break  # 一旦检测到程序运行，退出循环

        time.sleep(5)  # 每5秒检测一次

# 隐藏主窗口
def hide_console():
    # 通过调用 Windows API 隐藏控制台窗口
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

if __name__ == "__main__":
    hide_console()  # 隐藏控制台窗口
    setup_tray_icon()  # 设置托盘图标
#github：https://github.com/4x-China/
#哔哩哔哩：https://space.bilibili.com/1431664113?spm_id_from=333.337.0.0
#QQ群：861822298
#本代码为开源项目一切后果自负