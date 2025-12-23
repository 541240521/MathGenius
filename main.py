import sys
import os

# 针对 Windows 打包环境的 DLL 路径补丁
if sys.platform == 'win32' and getattr(sys, 'frozen', False):
    # 获取程序运行目录
    base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    # 显式添加 Qt 插件和 DLL 搜索路径
    qt_path = os.path.join(base_path, "PyQt6", "Qt6", "bin")
    if os.path.exists(qt_path):
        os.add_dll_directory(qt_path)
    
    # 备选路径（针对 onedir 模式）
    internal_path = os.path.join(base_path, "_internal", "PyQt6", "Qt6", "bin")
    if os.path.exists(internal_path):
        os.add_dll_directory(internal_path)

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # PyQt6 handles High DPI automatically, but we can set the style
    app.setApplicationName("MathGenius PRO")
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
