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
