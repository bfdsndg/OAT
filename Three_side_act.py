from Setting import logger,CONFIG
import Click
import time

def handle_center(adb_path,adb_port):
    logger.info("执行center状态的逻辑")

def handle_up(adb_path,adb_port):
    logger.info("执行up状态的逻辑")
    Click.click.adb_click(947,108,adb_path,adb_port) 
    time.sleep(1)
    Click.click.adb_click(947,108,adb_path,adb_port) 
    time.sleep(1)

def handle_down(adb_path,adb_port):
    logger.info("执行down状态的逻辑")
    for i in range(3):
        Click.click.adb_click(961,863,adb_path,adb_port) 
        time.sleep(1)

def handle_right(adb_path,adb_port):
    logger.info("执行right状态的逻辑")
    Click.click.adb_click(1810,108,adb_path,adb_port)

def handle_default(adb_path,adb_port):
    logger.info("未知状态/未开始，执行默认逻辑")

side_actions = {
    "center": handle_center,
    "up": handle_up,
    "down": handle_down,
    "right": handle_right
}

# current_side = "right" 
# side_actions.get(current_side, handle_default)(CONFIG.adb_path,CONFIG.adb_port) 