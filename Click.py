import subprocess
import os
import time
import numpy as np
import ADBScreenShot
from main import CONFIG, logger

"""
点击
出于设备的不固定延迟，暂时不考虑加入滑动（取消注释）
"""

class click:
    @staticmethod
    def adb_click(x, y, 
        adb_path=CONFIG["adb"]["path"],
        port=CONFIG["adb"]["port"]):
        """
        通过ADB在指定端口的设备上执行后台点击操作
        """
        if not os.path.exists(adb_path):
            return False, f"ADB文件不存在：{adb_path}"
        
        commands = [
            f'"{adb_path}" connect 127.0.0.1:{port}',  # 连接设备
            f'"{adb_path}" -s 127.0.0.1:{port} shell input tap {x} {y}'  # 发送点击
        ]
        
        # 执行命令并捕获输出
        for cmd in commands:
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10
                )
                output = result.stdout.strip()
            except subprocess.TimeoutExpired:
                return False, f"命令执行超时：{cmd}"
            except subprocess.CalledProcessError as e:
                # 捕获命令执行失败
                error_msg = e.stderr.strip() or f"命令执行失败，返回码：{e.returncode}"
                return False, f"执行命令出错：{cmd}\n{error_msg}"
            except Exception as e:
                return False, f"未知错误：{str(e)}"
        
        return True, f"成功点击坐标：({x}, {y})"
    
# class Draw:   # 目前用不到先注释掉了
#     @staticmethod
#     def adb_drag_touchscreen(
#         start_x, start_y, end_x, end_y,
#         adb_path=r"D:\Apps\MuMu\MuMu Player 12\shell\adb.exe",
#         port=16384
#     ):
#         """"""
#         cmd = (
#             f'"{adb_path}" -s 127.0.0.1:{port} shell '
#             f'input touchscreen swipe {start_x} {start_y} {end_x} {end_y} 1000'
#         )
#         try:
#             subprocess.run(cmd, shell=True, check=True, timeout=10)
#             time.sleep(1.5)  # 等待滑动完成
#             return True, f"触控滑动完成：({start_x},{start_y})→({end_x},{end_y})"
#         except Exception as e:
#             return False, f"滑动失败：{str(e)}"
        
#     @staticmethod
#     def _single_slide(start_x, start_y, end_x, end_y, duration, adb_path, port):
#         """内部函数：执行单次ADB滑动（复用adb_drag_touchscreen逻辑）"""
#         cmd = (
#             f'"{adb_path}" -s 127.0.0.1:{port} shell '
#             f'input touchscreen swipe {start_x} {start_y} {end_x} {end_y} {duration}'
#         )
#         try:
#             subprocess.run(
#                 cmd, shell=True, check=True,
#                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                 text=True, timeout=15
#             )
#             return True
#         except subprocess.TimeoutExpired:
#             print(f"滑动命令超时：{cmd}")
#             return False
#         except subprocess.CalledProcessError as e:
#             error_msg = e.stderr.strip() or f"返回码：{e.returncode}"
#             print(f"滑动命令执行失败：{error_msg}")
#             return False
#         except Exception as e:
#             print(f"滑动未知错误：{str(e)}")
#             return False

#     @staticmethod
#     def _small_distance_overshoot_rebound(
#         current_x, current_y, target_x, target_y,
#         adb_path, port, overshoot_ratio=1.5, short_duration=500
#     ):
#         """内部函数：小距离超调+回弹补滑"""
#         # 计算超调终点
#         delta_x = target_x - current_x
#         delta_y = target_y - current_y
#         overshoot_x = int(target_x + delta_x * overshoot_ratio)
#         overshoot_y = int(target_y + delta_y * overshoot_ratio)
        
#         # 超调滑动
#         print(f"超调滑动：({current_x},{current_y}) → ({overshoot_x},{overshoot_y})（时长{short_duration}ms）")
#         Draw._single_slide(current_x, current_y, overshoot_x, overshoot_y, short_duration, adb_path, port)
#         time.sleep(short_duration / 1000 + 0.5)
        
#         # 回弹滑动
#         print(f"回弹滑动：({overshoot_x},{overshoot_y}) → ({target_x},{target_y})（时长{short_duration}ms）")
#         Draw._single_slide(overshoot_x, overshoot_y, target_x, target_y, short_duration, adb_path, port)
#         time.sleep(short_duration / 1000 + 0.5)
        
#         return target_x, target_y

# class Key:
#     @staticmethod
#     def adb_keyboard_input(text_or_key, adb_path=r"D:\Apps\MuMu\MuMu Player 12\shell\adb.exe", port=16384):
#         """
#         """
#         if not os.path.exists(adb_path):
#             return False, f"ADB文件不存在：{adb_path}"
        
#         connect_cmd = f'"{adb_path}" connect 127.0.0.1:{port}'
        
#         # 特殊按键列表
#         special_keys = {"enter", "delete", "del", "backspace", "home", "menu", 
#                         "volume_up", "volume_down", "power"}
        
#         if text_or_key in special_keys:
#             keycode_map = {
#                 "enter": 66,
#                 "delete": 67,
#                 "del": 67,
#                 "backspace": 67,
#                 "home": 3,
#                 "menu": 82,
#                 "volume_up": 24,
#                 "volume_down": 25,
#                 "power": 26
#             }
#             keycode = keycode_map[text_or_key]
#             input_cmd = f'"{adb_path}" -s 127.0.0.1:{port} shell input keyevent {keycode}'
#         else:
#             # 发送普通文本
#             escaped_text = text_or_key.replace(" ", "%s")
#             input_cmd = f'"{adb_path}" -s 127.0.0.1:{port} shell input text {escaped_text}'
        
#         commands = [connect_cmd, input_cmd]
        
#         # 执行命令并捕获结果
#         for cmd in commands:
#             try:
#                 result = subprocess.run(
#                     cmd,
#                     shell=True,
#                     check=True,
#                     stdout=subprocess.PIPE,
#                     stderr=subprocess.PIPE,
#                     text=True,
#                     timeout=10
#                 )
#                 output = result.stdout.strip()
#             except subprocess.TimeoutExpired:
#                 return False, f"命令执行超时：{cmd}"
#             except subprocess.CalledProcessError as e:
#                 error_msg = e.stderr.strip() or f"返回码：{e.returncode}"
#                 return False, f"执行命令出错：{cmd}\n{error_msg}"
#             except Exception as e:
#                 return False, f"未知错误：{str(e)}"
        
#         return True, f"成功输入：{text_or_key}"