import easyocr
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import sys
from typing import List, Dict, Optional
from Setting import get_resource_path, logger  # 复用之前的路径适配函数

"""
OCR
"""

class Core:
    """基于EasyOCR的文字识别工具"""

    @staticmethod
    def draw_ocr(image: np.ndarray, boxes: list, txts: list, scores: list, 
                 font_path: Optional[str] = None, drop_score: float = 0.5) -> np.ndarray:
        """自定义绘制OCR标注, 基础函数无需理会"""
        if isinstance(image, np.ndarray):
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype(font_path, 20) if font_path else ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        for box, txt, score in zip(boxes, txts, scores):
            if score < drop_score:
                continue
            box = np.array(box).astype(np.int32)
            draw.polygon(box.flatten().tolist(), outline=(0, 255, 0), width=2)
            draw.text((box[0][0], box[0][1] - 20), f"{txt} ({score:.2f})", 
                      font=font, fill=(0, 0, 255))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def recognize_image_text(img_path: str, 
                             font_path: str = "simhei.ttf", 
                             drop_score: float = 0.5) -> List[Dict]:
        """核心文字识别,该函数需要一定时间运行,效率不高"""
        # 检查图片路径(应该不会出问题)
        # 初始化EasyOCR
        try:
            model_path = get_resource_path(".EasyOCR")
            reader = easyocr.Reader(
                ['ch_sim', 'en'], 
                gpu=True,  # 保持你的GPU设置（如果环境不支持，改成False）
                model_storage_directory=model_path,  # 本地模型路径
                download_enabled=False  # 禁用自动下载
            )
        except Exception as e:
            logger.error(f"EasyOCR初始化失败：{str(e)}")
            return []
        
        try:
            # result结构：[[bbox, text, score], ...]
            result = reader.readtext(img_path, detail=1, paragraph=False)
        except Exception as e:
            logger.error(f"识别失败：{str(e)}")
            return []
        
        if not result or len(result) == 0:
            logger.warning("未识别到任何文字")
            return []

        text_results = []
        boxes, txts, scores = [], [], []
        for item in result:
            bbox = item[0]  # 边界框：[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            text = item[1].strip()
            confidence = round(item[2], 2)
            
            if confidence < drop_score or not text:
                continue
            
            center_x = int((bbox[0][0] + bbox[2][0]) / 2)
            center_y = int((bbox[0][1] + bbox[2][1]) / 2)
            
            text_results.append({
                "text": text,
                "confidence": confidence,
                "position": {
                    "bbox": bbox,
                    "center": (center_x, center_y)
                }
            })
            boxes.append(bbox)
            txts.append(text)
            scores.append(confidence)
        print(text_results)
        return text_results

    @staticmethod
    def find_target_text(results: List[Dict], target_text: str, fuzzy: bool = True) -> Optional[Dict]:
        """查找目标文字（支持模糊匹配）
        :param results: 文字识别结果列表，使用 recognize_image_text 方法获得
        :param target_text: 目标文字内容
        :param fuzzy: 是否启用模糊匹配（包含即匹配成功）
        :return: 找到返回对应结果字典,未找到返回None
        """
        for res in results:
            if fuzzy:
                if target_text in res["text"]:
                    return res
            else:
                if res["text"] == target_text:
                    return res
        print(f"未找到目标文字：{target_text}")
        return None

    @staticmethod
    def recognize_image_text_re(
        img_path: str, 
        font_path: str = "simhei.ttf", 
        drop_score: float = 0.5,
        allowlist: bool = False,  # 是否仅识别数字
        roi_coords: tuple = None,  # 手动坐标 (x1, y1, x2, y2)
    ) -> List[Dict]:
        """核心文字识别"""
        # 校验文件
        if not os.path.exists(img_path):
            print(f"图片文件不存在：{img_path}")
            return None
        if os.path.getsize(img_path) < 1024:
            print(f"图片文件无效（大小<1KB）：{img_path}")
            return None
        
        img = cv2.imread(img_path)
        if img is None:
            print(f"图片读取失败：{img_path}")
            return None
        
        cropped_img = img  # 默认为原图
        h, w = img.shape[:2]  # 获取图片高、宽
        
        if roi_coords:
            # 手动坐标裁剪：(x1, y1, x2, y2)
            x1, y1, x2, y2 = roi_coords
            
            x1 = max(0, min(int(x1), w-1))
            y1 = max(0, min(int(y1), h-1))
            x2 = max(x1+1, min(int(x2), w))
            y2 = max(y1+1, min(int(y2), h))
            cropped_img = img[y1:y2, x1:x2]  
            # print(f"已按坐标裁剪：({x1},{y1})-({x2},{y2})")
        # 初始化EasyOCR
        try:
            model_path = get_resource_path(".EasyOCR")
            reader = easyocr.Reader(
                ['ch_sim', 'en'], 
                gpu=True,  # 保持你的GPU设置（如果环境不支持，改成False）
                model_storage_directory=model_path,  # 指定本地模型路径
                download_enabled=False  # 禁用自动下载
            )
            # print("EasyOCR初始化成功")
        except Exception as e:
            print(f"EasyOCR初始化失败：{str(e)}")
            return None
        
        # 执行识别
        try:
            if allowlist:
                # 仅识别数字
                result = reader.readtext(
                    cropped_img,  
                    detail=1, 
                    paragraph=False,
                    allowlist='0123456789'
                )
                print(1)
            else:
                result = reader.readtext(
                    cropped_img,  
                    paragraph=False
                )
        except Exception as e:
            print(f"识别失败：{str(e)}")
            return None
        
        if not result:
            print("未识别到任何文字")
            return None

        # 解析结果
        text_results = []
        boxes, txts, scores = [], [], []
        # 裁剪偏移量
        x_offset = x1 if (roi_coords ) else 0
        y_offset = y1 if (roi_coords ) else 0
        
        for item in result:
            bbox = item[0]  # 裁剪图中的边界框：[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            text = item[1].strip()
            confidence = round(item[2], 2)
            
            if confidence < drop_score or not text:
                continue
            
            original_bbox = [
                [p[0] + x_offset, p[1] + y_offset] for p in bbox
            ]
            center_x = int((original_bbox[0][0] + original_bbox[2][0]) / 2)
            center_y = int((original_bbox[0][1] + original_bbox[2][1]) / 2)
            
            text_results.append({
                "text": text,
                "confidence": confidence,
                "position": {
                    "bbox": original_bbox,  # 原图中的边界框
                    "center": (center_x, center_y)  # 原图中的中心坐标
                }
            })
            boxes.append(original_bbox)
            txts.append(text)
            scores.append(confidence)

        return text_results



