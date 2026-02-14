import subprocess
import os
from typing import Optional
from main import CONFIG, logger

"""
截屏
"""

class Core:
    Adb_path = '0'
    Adb_port = 0
    
    @staticmethod
    def adb_screenshot( save_path=CONFIG["resource"]["screenshot_path"],
        adb_path=CONFIG["adb"]["path"],
        adb_port=CONFIG["adb"]["port"]) -> bool:
        """
        通过指定的ADB路径和端口，截取模拟器屏幕
        :param adb_path: 验证后的ADB路径
        :param adb_port: 验证后的ADB端口
        :param save_path: 截图保存路径
        :return: 成功返回True，失败返回False
        """
        try:
        # 连接目标模拟器（指定端口）
            connect_cmd = f'"{adb_path}" connect 127.0.0.1:{adb_port}'
            connect_result = subprocess.run(
            connect_cmd, shell=True, capture_output=True, text=True, timeout=10
            )
        
            if "failed" in connect_result.stderr.lower() or "unable" in connect_result.stderr.lower():
                logger.error(f"连接模拟器失败！原因：{connect_result.stderr.strip()}")
                return False

        # 执行截图（保存到模拟器内部）
            screenshot_cmd = f'"{adb_path}" -s 127.0.0.1:{adb_port} shell screencap -p /sdcard/temp_screenshot.png'
            subprocess.run(screenshot_cmd, shell=True, capture_output=True, timeout=15)
            # print("截图成功")
        # 拉取截图到电脑
            pull_cmd = f'"{adb_path}" -s 127.0.0.1:{adb_port} pull /sdcard/temp_screenshot.png "{save_path}"'
            subprocess.run(pull_cmd, shell=True, capture_output=True, timeout=15)
        
        # 删除模拟器内临时文件
            delete_cmd = f'"{adb_path}" -s 127.0.0.1:{adb_port} shell rm /sdcard/temp_screenshot.png'
            subprocess.run(delete_cmd, shell=True, capture_output=True, timeout=10)
        
        # 验证截图是否有效
            if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                # print(f"\n截图成功")
                # logger.info(f"保存路径：{save_path}")
                return True
            else:
                logger.error(f"截图失败：未生成有效图片")
                return False
    
        except Exception as e:
            logger.error(f"截图过程异常：{str(e)}")

            return False
