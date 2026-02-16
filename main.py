from Setting import CONFIG, logger, check_env, get_exe_dir
import time
import ADBScreenShot
import CharRecogise
import Click  
import Compare
import Dic
import os
import GLre
import TimeJudge
from PIL import Image
from concurrent import futures
import datetime
import threading # 其实不用多线程还根高效，或者是我没想好怎么用，考虑在第三版的复用
import subprocess

CONSIDER_BREAK = CONFIG["delay"]["consider_break"]  
SHORT_BREAK = CONFIG["delay"]["short_break"]
MID_BREAK = CONFIG["delay"]["mid_break"]
LONG_BREAK = CONFIG["delay"]["long_break"]
WAIT_TIME = CONFIG["delay"]["Wait_time"]
LIMIT_GROUP = CONFIG["limit"]["group"] 
ACC_LEVEL = CONFIG["acc"]["level"]

"""
OATg 第二版放弃了识别时间的写法，改成了采用固定时间的思路
"""



def Where_I_am(adb_path_input: str, adb_port_input: int, save_path: str = CONFIG["resource"]["screenshot_path"]) -> str:
    logger.info("===========Where_I_am开始执行============")
    Judge = ADBScreenShot.Core.adb_screenshot(save_path, adb_path_input, adb_port_input)
    if not Judge:
        logger.error("截图失败，无法判断位置")
        return None
    list1 = ["Search", "Military", "Home", "Map", "Right_attack", "Monster"]
    for name in list1:
        Judge = check_only_Mu(1, adb_path_input, adb_port_input, name, save_path)
        if Judge:
            return name
    
def Back_to_Main(times:int,adb_path_input:str,adb_port_input:int,save_path=CONFIG["resource"]["screenshot_path"])->bool:
    """"""
    times+=2
    if times > 3:
        return False
    astr = Where_I_am(adb_path_input,adb_port_input,save_path)
    print(f"当前位置为：{astr}")
    if astr is None:
        return False    
    if astr == "Military":
        Click.click.adb_click(85,160,adb_path_input,adb_port_input)
        time.sleep(SHORT_BREAK)
        Back_to_Main(times-1,adb_path_input, adb_port_input)
    elif astr == "Home":     
        Click.click.adb_click(85,160,adb_path_input,adb_port_input)
        time.sleep(SHORT_BREAK)
        Back_to_Main(times-1,adb_path_input, adb_port_input)
    elif astr == "Map":
        Click.click.adb_click(85,160,adb_path_input,adb_port_input)
        time.sleep(SHORT_BREAK)
        Back_to_Main(times-1,adb_path_input, adb_port_input)
    elif astr == "Right_attack":
        Click.click.adb_click(85,160,adb_path_input,adb_port_input)
        time.sleep(SHORT_BREAK)
        Back_to_Main(times-1,adb_path_input, adb_port_input) 
    elif astr == "Monster":
        Click.click.adb_click(85,160,adb_path_input,adb_port_input)
        time.sleep(SHORT_BREAK)
        Back_to_Main(times-1,adb_path_input, adb_port_input)
    elif astr == "Search":
        return True
    Judge1 = check_only_quick(1,adb_path_input,adb_port_input,"Search")
    if Judge1 == False:
        Back_to_Main(times,adb_path_input, adb_port_input)
    return True
    
def check_only_Mu(times:int,adb_path_input:str,adb_port_input:int,asset_name:str,save_path=CONFIG["resource"]["screenshot_path"])->bool:
    """"""
    astr = "Asset\\" + asset_name + ".png"
    bstr = asset_name + ".png"
    Judge, center = Compare.Com.match_button_slide(astr,save_path,Dic.Dic.dictionary[bstr][0],
                                        Dic.Dic.dictionary[bstr][1])
    if not Judge:
        return False
    return True

def check_only(times:int,adb_path_input:str,adb_port_input:int,asset_name:str,save_path=CONFIG["resource"]["screenshot_path"])->bool:
    """"""
    astr = "Asset\\" + asset_name + ".png"
    bstr = asset_name + ".png"
    Judge = ADBScreenShot.Core.adb_screenshot(save_path,adb_path_input,adb_port_input)
    if not Judge:
        print("截图失败，重新尝试")
        return False
    Judge, center = Compare.Com.match_button_slide(astr,save_path,Dic.Dic.dictionary[bstr][0],
                                        Dic.Dic.dictionary[bstr][1])
        
    if not Judge:
        print(f"未找到目标{asset_name}重新尝试")
        time.sleep(1)
        Judge, center = Compare.Com.match_button_slide(astr,save_path,Dic.Dic.dictionary[bstr][0],
                                                Dic.Dic.dictionary[bstr][1])
        if Judge : 
            print(f"找到目标{asset_name}")
            return True
        if not Judge:
            return False
    return True

def check_only_quick(times:int,adb_path_input:str,adb_port_input:int,asset_name:str,save_path=CONFIG["resource"]["screenshot_path"])->bool:
    """"""
    astr = "Asset\\" + asset_name + ".png"
    bstr = asset_name + ".png"
    ADBScreenShot.Core.adb_screenshot(save_path,adb_path_input,adb_port_input)
    Judge, center = Compare.Com.match_button_slide(astr,save_path,Dic.Dic.dictionary[bstr][0],
                                        Dic.Dic.dictionary[bstr][1])
    if not Judge:
        return False
    return True

def check_click(times:int,adb_path_input:str,adb_port_input:int,asset_name:str,save_path=CONFIG["resource"]["screenshot_path"])->bool:
    """
    check_click 的 Docstring
    
    :param times: 运行次数
    :type times: int
    :param adb_path_input: adb路径
    :type adb_path_input: str
    :param adb_port_input: adb端口
    :type adb_port_input: str
    :param asset_name: 图形名字
    :type asset_name: str
    :return: True表示成功，False表示失败
    :rtype: bool
    """
    Judge1 = True
    astr = "Asset\\" + asset_name + ".png"
    bstr = asset_name + ".png"
    Judge = ADBScreenShot.Core.adb_screenshot(save_path,adb_path_input,adb_port_input)
    if not Judge:
        print("截图失败，重新尝试")
        return False


    Judge, center = Compare.Com.match_button_slide(astr,save_path,Dic.Dic.dictionary[bstr][0],
                                        Dic.Dic.dictionary[bstr][1])
        
    if not Judge:
        print(f"未找到目标{asset_name}重新尝试")
        time.sleep(1)
        for i in range(3):
            Judge = ADBScreenShot.Core.adb_screenshot(save_path,adb_path_input,adb_port_input)
            Judge, center = Compare.Com.match_button_slide(astr,save_path,Dic.Dic.dictionary[bstr][0],
                                                Dic.Dic.dictionary[bstr][1])
            if Judge : break
            time.sleep(3)
            if i==2 and not Judge:
                print("连续三次未找到目标")
                Judge1 = False
                break 
        if not Judge1:
            return False         


    Judge, astr = Click.click.adb_click(center[0],center[1],adb_path_input,adb_port_input)
    if not Judge:
        Judge, astr = Click.click.adb_click(center[0],center[1],adb_path_input,adb_port_input)
        if not Judge:
            return False
    return True

def name_click(times:int,adb_path_input:str,adb_port_input:int,asset_name:str)->bool:
    """
    """
    center = Dic.Dic.dictionary[asset_name][0]
    Judge, out = Click.click.adb_click(center[0],center[1],adb_path_input,adb_port_input)
    if not Judge:
        return False
    return True
     
def create_folder(folder_name="ahh"):
    """
    在下一路径创建文件夹
    :param folder_name: 文件夹名称
    :return: 创建成功返回文件夹路径,失败返回None
    """
    current_path = os.getcwd()
    create_path = os.path.join(current_path, "Shoot")
    folder_path = os.path.join(create_path, folder_name)
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"文件夹创建成功：{folder_path}")
        return folder_path
    except Exception as e:
        print(f"文件夹创建失败：{e}")
        return None
    
def check_png(times:int,adb_path_input:str,adb_port_input:int,save_path=CONFIG["resource"]["screenshot_path"])->bool:
    """
    过不了就完蛋了
    """
    Judge = ADBScreenShot.Core.adb_screenshot(save_path,adb_path_input,adb_port_input)
    if not Judge:
        print("怎么连截图都过不了？")
        return False
    try:
        with Image.open(save_path) as img:
            width, height = img.size
            return width == 1920 and height == 1080
    except Exception as e:
        print(f"图片处理错误: {e}")
        return False
    
def One_Circle(times:int, adb_path_input:str,adb_port_input:int,attack:int,G_list:list,G_list_M:list,save_path=CONFIG["resource"]["screenshot_path"])->tuple:
    """一个循环,return None 表示失败"""
    # 主堡判断
    Judge1 = check_only_quick(times,adb_path_input,adb_port_input,"House",save_path)
    Judge2 = check_only_quick(times,adb_path_input,adb_port_input,"Search",save_path)
    if Judge1 and Judge2:
        logger.info("未处于主城状态")
        Judge1 = check_click(times,adb_path_input,adb_port_input,"House",save_path)
    if Judge1 == False:
        logger.info("处于主城状态")
    if Judge2 == False:
        logger.error("我是谁？我在哪？我要干什么？")
        return None,None

    time.sleep(SHORT_BREAK)
        # 搜索：
    Judge1 = check_click(times,adb_path_input,adb_port_input,"Search",save_path)
    if not Judge1:
        logger.error("点击搜索失败")
    time.sleep(CONSIDER_BREAK) 
    # (74，504)->对应魔兽
    # Click.click.adb_click(74,504,adb_path_input,adb_port_input)
    Judge1 = check_click(times,adb_path_input,adb_port_input,"Monster",save_path)
    if not Judge1:
        logger.error("点击魔兽失败")
    logger.info("点击魔兽成功")
    time.sleep(CONSIDER_BREAK)   

    Circle = True
    # 搜索循环
    while Circle:     
        time.sleep(CONSIDER_BREAK)    
        #  (606,663)->确定搜索
        Click.click.adb_click(606,663,adb_path_input,adb_port_input)
        logger.info("点击确定搜索成功")

        time.sleep(SHORT_BREAK)

        # 进入是否已打识别
        Circle, G_list = GLre.Core.check_have_attack(G_list,adb_path_input,adb_port_input,save_path)
        if G_list is None:
            print("识别是否已打失败")
            G_list = G_list_M.copy()
            Judge2 = False
            break
        G_list_M = G_list.copy()
        time.sleep(CONSIDER_BREAK)  
    if Judge2==False:
        return None,None
    
    # (962,534)->点击一个魔兽
    Click.click.adb_click(962,534,adb_path_input,adb_port_input)
    logger.info("点击一个魔兽成功")
    time.sleep(CONSIDER_BREAK)  

    Judge1 = check_click(times,adb_path_input,adb_port_input,"Attack",save_path)
    if not Judge1:
        logger.error("点击扫荡失败")
        return None,None

    time.sleep(CONSIDER_BREAK)  

        # (1766,878)->扫荡
    Judge1 = check_click(times,adb_path_input,adb_port_input,"Right_attack",save_path)
    if not Judge1:
        logger.error("点击右侧扫荡失败")
        return None,None
    attack += 1
    logger.info("点击扫荡成功")

    time.sleep(CONSIDER_BREAK)     

    quit = Back_to_Main(0, adb_path_input,adb_port_input)
    if quit == False:
        return None,None
    time.sleep(SHORT_BREAK)

    return attack, G_list

def Mili_uppppp(adb_path_input:str,adb_port_input:int,used:int,
                times:int,save_path=CONFIG["resource"]["screenshot_path"]):
    """补兵功能"""
    logger.info("==========进入补兵内部分界线===========")
    Judge1 = Back_to_Main(0, adb_path_input,adb_port_input,save_path)
    if Judge1 == False:
        logger.error("返回主界面失败")
        return None, None
    # (1842,857)->内城
    logger.info("点击内城")
    Click.click.adb_click(1842,857,adb_path_input,adb_port_input)
    time.sleep(SHORT_BREAK)
    Judge1 = check_only(times,adb_path_input,adb_port_input,"Home",save_path)
    if Judge1==False:
        return None, None
    logger.info("点击内城成功")


    #(1676,395)->编队
    Click.click.adb_click(1676,395,adb_path_input,adb_port_input)

    time.sleep(SHORT_BREAK)

    Judge1 = check_only(times,adb_path_input,adb_port_input,"Military",save_path)
    if Judge1 == False:
        logger.error("给我干哪来了？")
    logger.info("点击编队成功")

    Judge1 = check_only(times,adb_path_input,adb_port_input,"Energy1",save_path)
    while Judge1 == True:
        logger.info("体力不足")
        #(1770,890)->取消编队
        Click.click.adb_click(1770,890,adb_path_input,adb_port_input)
        logger.info("点击取消编队成功")
        # if used >= 1:
        #     used -= 1
        time.sleep(SHORT_BREAK)
        Click.click.adb_click(164,408,adb_path_input,adb_port_input)
        time.sleep(SHORT_BREAK)
        Judge1 = check_only(times,adb_path_input,adb_port_input,"Energy1",save_path)
    
    if Judge1 == False:
        if used >= LIMIT_GROUP:
            logger.warning("补兵次数达到上限，无法继续补兵")
            return used, None
        Judge2 = check_click(times,adb_path_input,adb_port_input,"Plus",save_path)
        if Judge2 == False:
            logger.warning("无补兵按钮")
            if used == 0:
                logger.info("程序完成")
                return -1, None
            return used, 0
    # (1760,720)->补兵
        logger.info("点击补兵成功")
        used += 1
        time.sleep(SHORT_BREAK)

    Judge1 = Back_to_Main(0, adb_path_input,adb_port_input)
    if Judge1 == False:
        logger.error("返回主界面失败")
        return None,None
    return used, None

def Main():
    if not check_env():
        logger.error("环境检查未通过，程序终止")
        return
    End = False
    adb_path_input = CONFIG["adb"]["path"]
    adb_port_input = CONFIG["adb"]["port"]
    exe_dir = get_exe_dir()
    save_path = os.path.join(exe_dir, CONFIG["resource"]["screenshot_path"])
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    times = 1
    Judge1 = True
    Judge2 = True
    Circle = True
    G_list = []
    G_list_M = []
    Time_list = []
    Time_list_temp = []
    Time_list_back = []
    used = 0
    used_temp = 0
    inner_times = 0
    attack = 0
    attack_conside = 0
    Judge = check_png(0,adb_path_input,adb_port_input,save_path)
    callfinish = False
    positive_nums = []
    last_nums = 0
    if Judge == False:
        logger.error("...程序结束，截图或者分辨率有误...")
        End = True

    while not End:
        while used < LIMIT_GROUP and Circle:
            Judge = Back_to_Main(0, adb_path_input,adb_port_input,save_path)
            if Judge == False:
                logger.error("返回主界面失败")
                End = True
                Judge1 = False
                break
            time.sleep(CONSIDER_BREAK)
            used, _ = Mili_uppppp(adb_path_input,adb_port_input,used,times,save_path) 
            if used is not None:
                used_temp = used   
            if used is None:
                used = used_temp
                logger.info("补兵环节...重新循环...")
                # End = True
                break
            if used == -1: # 表示完成。主堡没编队且在外编队480秒没返回
                End = True
                break
            if _ is not None: # 意味着主堡没编队但是在外又存在编队
                Circle = False # 我需要记录used的值，用在减法上面，进入逻辑2，又好像不用
                break
            attack, G_list = One_Circle(times,adb_path_input,adb_port_input,attack,G_list,G_list_M,save_path)
            if G_list is None:
                G_list = G_list_M.copy()
            if attack is not None:
                attack_conside = attack
            if attack is None:
                attack = attack_conside
                used -= 1
                logger.info("Circle环节...重新循环...")
                # End = True
                break
            time.sleep(CONSIDER_BREAK)
            times += 1
            pass

        if used >= LIMIT_GROUP and Circle:
            wait_time = WAIT_TIME + times * 20 if WAIT_TIME + times * 20 < 240 else 240
            wait_time1 = wait_time / (1+ACC_LEVEL/10)
            logger.info(f"进入等待时间，等待{wait_time1}+{wait_time}秒")
            time.sleep(wait_time1 + wait_time)
            used = 0
        pass

        while not Circle:
            if used == 0:
                End = True
                break
            if inner_times == 0:
                logger.info("==========进入逻辑2部分界线===========")
                logger.info("进入等待时间")
                wait_time = WAIT_TIME + times * 20 if WAIT_TIME + times * 20 < 240 else 240
                wait_time1 = wait_time / (1+ACC_LEVEL/10)
                logger.info(f"进入等待时间，等待{wait_time1}+{wait_time}秒")
                time.sleep(wait_time1 + wait_time)
                used_temp = used # 在首次赋予
                inner_times += 1
                used = 0

            Judge = Back_to_Main(0, adb_path_input,adb_port_input,save_path)
            if Judge == False:
                logger.error("返回主界面失败")
                End = True
                break
            time.sleep(CONSIDER_BREAK)

            while used <= used_temp:
                used, _ = Mili_uppppp(adb_path_input,adb_port_input,used,times,save_path)
                if used is not None:
                    used_temp = used   
                if used is None:
                    used = used_temp
                    logger.info("补兵环节...重新循环...")
                    # End = True
                    break
                if used == -1: # 表示完成。主堡没编队且在外编队480秒没返回
                    End = True
                    break
                if _ is not None: # 意味着主堡没编队但是在外又存在编队
                    inner_times = 0 # 我需要记录used的值，用在减法上面，进入逻辑2
                    break

                attack, G_list = One_Circle(times,adb_path_input,adb_port_input,attack,G_list,G_list_M,save_path)
                if G_list is None:
                    G_list = G_list_M.copy()
                if attack is not None:
                    attack_conside = attack
                if attack is None:
                    attack = attack_conside
                    used -= 1
                    logger.info("Circle环节...重新循环...")
                    # End = True
                    break
                time.sleep(CONSIDER_BREAK)
                pass

            if used >= used_temp:
                wait_time = WAIT_TIME + times * 20 if WAIT_TIME + times * 20 < 240 else 240
                wait_time1 = wait_time / (1+ACC_LEVEL/10)
                logger.info(f"进入等待时间，等待{wait_time1}+{wait_time}秒")
                time.sleep(wait_time1 + wait_time)
                used = 0


if __name__ == "__main__":

    Main()
