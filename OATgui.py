'''
OATgui 的 Docstring
'''

from PySide2.QtWidgets import QApplication, QWidget, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QThread, Signal, Slot
import yaml
from Setting import CONFIG, logger, get_resource_path, get_exe_dir
import time
from main import Main
import threading
import os

class Running(QThread):
    log_signal = Signal(str)
    error_signal = Signal(str)
    finish_signal = Signal()
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            self.log_signal.emit("start running")
            Main()
            self.finish_signal.emit()
        except Exception as e:
            self.error_signal.emit(f"run error: {e}")
            logger.error(e)

class OATgui():
    def __init__(self):
        ui_path = get_resource_path("OATg.ui")
        self.ui = QUiLoader().load(ui_path)
        self.init_config()
        self.ui.b_config_save.clicked.connect(self.save_config)
        self.ui.c_acc_level.currentIndexChanged.connect(self.read_user_c_change)
        self.ui.b_start.clicked.connect(self.run)
        self.main_thread = None
        self.ui.t_error_show.clear()
    
    def save_config(self):
        try:
            adb_path = self.ui.t_adb_path.toPlainText()
            adb_port = int(self.ui.t_adb_port.toPlainText())
        except Exception as e:
            self.log_error(f"save_config error: {e}")
            self.log_error("\n请检查adb路径和端口是否正确")
            logger.error(e)

        # print(adb_path, adb_port)

        yaml_path = r'config\app_config.yaml'
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                config['adb']['path'] = adb_path
                config['adb']['port'] = adb_port
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, indent=2, encoding='utf-8', allow_unicode=True, sort_keys=False)
            QMessageBox.information(self.ui, '提示', '保存成功！')
        except Exception as e :
            self.log_error(f"save_config error: {e}")
            logger.error(e)
    
    def init_config(self):
        yaml_path = r'config\app_config.yaml'
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                adb_path = config['adb']['path']
                adb_port = config['adb']['port']
                self.ui.t_adb_path.setPlainText(adb_path)
                self.ui.t_adb_port.setPlainText(str(adb_port))
        except Exception as e:
            self.log_error(f"init_config error: {e}")
            logger.error(e)
    
    def read_user_c_change(self):
        acc = 0
        acc_level = self.ui.c_acc_level.currentText()
        if acc_level == '内政加速0':
            acc = 0
        elif acc_level == '内政加速20%':
            acc = 1
        elif acc_level == '内政加速40%':
            acc = 2
        elif acc_level == '内政加速60%':
            acc = 3
        elif acc_level == '内政加速80%':
            acc = 4
        elif acc_level == '内政加速100%':
            acc = 5
        else:
            logger.error('acc_level error')
            raise ValueError('acc_level error')
        try:
            with open(r'config\app_config.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                config['acc']['level'] = acc
            with open(r'config\app_config.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(config, f, indent=2, encoding='utf-8', allow_unicode=True, sort_keys=False)
        except Exception as e:
            self.log_error(f"read_user_c_change error: {e}")
            logger.error(e)
    
    def log_error(self, error_msg):
        self.ui.t_error_show.append(f"current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - log error- {error_msg}")

    def run(self):
        if self.main_thread is not None and self.main_thread.isRunning():
            self.log_error("程序正在运行中，请等待程序结束后再运行")
            return
        
        self.main_thread = Running()
        
        self.main_thread.error_signal.connect(self.log_error)
        self.main_thread.finish_signal.connect(lambda: QMessageBox.information(self.ui, "完成", "ADB操作执行完毕！"))
        
        self.main_thread.start()
            

app = QApplication([])
appui = OATgui()
appui.ui.show()

app.exec_()
