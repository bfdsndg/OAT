import cv2
import numpy as np
from typing import Tuple, Optional, Union
import os
from Setting import get_resource_path,logger

"""
OpenCV
"""

class Com:   
    @staticmethod
    def match_button_center( # 其实我根本没用这个函数
        template_path: str,
        verify_img_path: str,
        activity_side_len: int ,
        activity_center: Tuple[int, int],      
        match_threshold: float = 0.85
    ) -> Tuple[bool, Optional[Tuple[int, int]]]:
        """
        在指定中心与边长正方形区域内匹配目标按钮
        :param template_path: 目标球状按钮的模板图路径（单独截取的按钮图）
        :param verify_img_path: 待验证的游戏截图路径
        :param activity_center: 活动区域中心坐标
        :param activity_side_len: 活动区域正方形边长
        :param match_threshold: 匹配度阈值（0-1，默认0.85，越高越精准）
        :return: 注意第二项返回值
        """
        # logger.info(f"开始匹配按钮：{template_path} {verify_img_path} {activity_center} {activity_side_len} {match_threshold}")
        template_path = get_resource_path(template_path)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            # 打印错误日志，方便排查
            raise FileNotFoundError(f"无法读取图片：{template_path}\n请检查：1. .spec是否打包了Asset文件夹 2. 图片路径是否正确")
        verify_img = cv2.imread(verify_img_path, cv2.IMREAD_GRAYSCALE)

        center_x, center_y = activity_center
        half_side = activity_side_len // 2
        # 活动区域坐标：x_start, y_start, x_end, y_end
        img_h, img_w = verify_img.shape[:2]
        x_start = max(0, center_x - half_side)
        y_start = max(0, center_y - half_side)
        x_end = min(img_w, center_x + half_side)
        y_end = min(img_h, center_y + half_side)
    
        activity_roi = verify_img[y_start:y_end, x_start:x_end]
    
        template_h, template_w = template.shape[:2]
    
        # 执行模板匹配
        match_result = cv2.matchTemplate(activity_roi, template, cv2.TM_CCOEFF_NORMED)
    
        max_match_val = np.max(match_result)
        if max_match_val < match_threshold:
            # print(f"识别失败")
            return False, None
    
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)
        roi_x, roi_y = max_loc 
        # 转换为原始图片的全局坐标
        global_x = x_start + roi_x + template_w // 2
        global_y = y_start + roi_y + template_h // 2
        target_pos = (global_x, global_y)

        # print(f"匹配成功")
        return True, target_pos
    
    @staticmethod
    def match_button_slide(
        template_path: str,
        verify_img_path: str,
        activity_topleft: Tuple[int, int],      
        activity_bottomright: Tuple[int, int],
        match_threshold: float = 0.85
    ) -> Tuple[bool, Optional[Tuple[int, int]]]:
        """
        在指定中心与边长正方形区域内匹配目标按钮
        :param template_path: 目标球状按钮的模板图路径（单独截取的按钮图）
        :param verify_img_path: 待验证的游戏截图路径
        :param match_threshold: 匹配度阈值（0-1，默认0.85，越高越精准）
        :return: 注意第二项返回值
        """

        # if os.path.exists(r"ScreenShotsource\source.png") and os.path.getsize(r"ScreenShotsource\source.png") > 0:
        #     print("source.png exists")
        # else:
        #     print("source.png not exists")
        #     return False, None
        # print(template_path,verify_img_path)
        # logger.info(f"开始匹配按钮：{template_path} {verify_img_path} ")
        template_path = get_resource_path(template_path)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            # 打印错误日志
            raise FileNotFoundError(f"无法读取图片：{template_path}\n请检查：1. .spec是否打包了Asset文件夹 2. 图片路径是否正确")
        verify_img = cv2.imread(verify_img_path, cv2.IMREAD_GRAYSCALE)

        # 活动区域坐标：x_start, y_start, x_end, y_end
        img_h, img_w = verify_img.shape[:2]
        x_start = max(0, activity_topleft[0])
        y_start = max(0, activity_topleft[1])
        x_end = min(img_w, activity_bottomright[0])
        y_end = min(img_h, activity_bottomright[1])
    
        activity_roi = verify_img[y_start:y_end, x_start:x_end]
    
        # 获取模板图尺寸
        template_h, template_w = template.shape[:2]
    
        match_result = cv2.matchTemplate(activity_roi, template, cv2.TM_CCOEFF_NORMED)

        max_match_val = np.max(match_result)
        if max_match_val < match_threshold:
            # print(f"识别失败")
            return False, None
    
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)
        roi_x, roi_y = max_loc  
        # 转换为原始图片的全局坐标
        global_x = x_start + roi_x + template_w // 2
        global_y = y_start + roi_y + template_h // 2
        target_pos = (global_x, global_y)

        # print(f"匹配成功")
        return True, target_pos

