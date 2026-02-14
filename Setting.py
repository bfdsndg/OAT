import yaml
import logging
import os
import sys

"""
设置
"""

def get_resource_path(relative_path):
    """
    获取资源的绝对路径：
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # 开发环境，基于当前脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_exe_dir():
    """获取EXE所在目录/脚本目录，用于写入文件"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# ================ 初始化日志 ==================
def init_logger():
    # 日志目录：打包后放到EXE同目录
    if getattr(sys, 'frozen', False):
        log_dir = os.path.join(os.path.dirname(sys.executable), "logs")
    else:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    logger = logging.getLogger("auto_tool")
    # 打印路径信息，方便排查
    logger.info(f"程序运行目录：{os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))}")
    logger.info(f"资源根目录：{get_resource_path('')}")
    return logger

logger = init_logger()

# ======================= 加载配置 ===================
def load_config():
    # 外部配置路径（EXE同目录的config文件夹）
    exe_dir = get_exe_dir()
    external_config_dir = os.path.join(exe_dir, "config")
    external_config_path = os.path.join(external_config_dir, "app_config.yaml")

    # 检查外部配置是否存在
    if not os.path.exists(external_config_path):
        error_msg = f"""
程序终止：未找到用户配置文件！
请按以下步骤操作：
1. 在 {exe_dir} 目录下新建「config」文件夹；
2. 将配置文件 app_config.yaml 放入该文件夹；
3. 重启程序。
当前缺失的配置文件路径：{external_config_path}
        """
        # 控制台输出
        print(error_msg)
        # 日志记录
        logger.fatal(error_msg)
        # 终止程序
        sys.exit(1)

    # 读取外部配置
    logger.info(f"加载用户自定义配置：{external_config_path}")
    with open(external_config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    # 修复配置中的资源路径
    config["resource"]["asset_path"] = get_resource_path(config["resource"]["asset_path"])
    config["resource"]["font_path"] = get_resource_path(config["resource"]["font_path"])
    return config

CONFIG = load_config()

# =================== 检查资源/ADB可用性 ================
def check_env():
    # 检查ADB路径（配置文件中用绝对路径，如D:\Apps\adb\adb.exe）
    if not os.path.exists(CONFIG["adb"]["path"]):
        logger.error(f"ADB路径无效：{CONFIG['adb']['path']}\n提示：请检查config/app_config.yaml中的adb.path配置")
        return False
    # 检查Asset资源（get_resource_path修复）
    if not os.path.exists(CONFIG["resource"]["asset_path"]):
        logger.error(f"Asset资源文件夹不存在：{CONFIG['resource']['asset_path']}\n提示：请检查.spec文件是否打包了Asset文件夹，或配置文件中的asset_path是否正确")
        return False
    # 检查字体文件（已修复）
    if not os.path.exists(CONFIG["resource"]["font_path"]):
        logger.error(f"字体文件不存在：{CONFIG['resource']['font_path']}\n提示：请检查.spec文件是否打包了字体文件，或配置文件中的font_path是否正确")
        return False
    logger.info("环境检查通过")
    return True