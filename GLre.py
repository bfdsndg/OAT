from PIL import Image
import numpy as np
import cv2
import CharRecogise
import time
import ADBScreenShot
import re
from Setting import get_resource_path,logger

"""
检查重复的功能函数
"""

class Core:
    @staticmethod
    def check_have_attack(list1:list,adb_path:str,adb_port:int,save_path:str):
        """不在就是false,用None判断是否正常运行"""
        Judge = ADBScreenShot.Core.adb_screenshot(save_path,adb_path,adb_port)
        if Judge == False:
            return True, None
        font_path = get_resource_path("DENG.TTF")
        temp_list = CharRecogise.Core.recognize_image_text_re(save_path,font_path,0.5,False,(1444,665,1535,691))
        if temp_list is None:
            return True, None
        nums = re.findall(r'\d+', temp_list[0]["text"]) # OCR读取然后匹配
        try:  # 改动
            position = (int(nums[0]),int(nums[1]))
            if position in list1:
                return True, list1
            if position not in list1:
                list1.append(position)
                return False, list1
        except IndexError:
            logger.error("匹配坐标出错")
            return True, None
    