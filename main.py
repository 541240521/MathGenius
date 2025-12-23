import sys
import os

# 针对 Windows 打包环境的 DLL 路径补丁
if sys.platform == 'win32' and getattr(sys, 'frozen', False):
    import os
    # 获取程序运行目录
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    
    # 强制将所有可能的 DLL 目录加入搜索路径
    # 包含根目录、_internal 目录以及 Qt 的 bin 目录
    possible_paths = [
        base_path,
        os.path.join(base_path, "_internal"),
        os.path.join(base_path, "PyQt6", "Qt6", "bin"),
        os.path.join(base_path, "_internal", "PyQt6", "Qt6", "bin"),
    ]
    
    for p in possible_paths:
        if os.path.exists(p):
            try:
                os.add_dll_directory(p)
            except Exception:
                pass

    # 某些情况下需要手动设置环境变量来隔离系统干扰
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(base_path, "PyQt6", "Qt6", "plugins")
    if not os.path.exists(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(base_path, "_internal", "PyQt6", "Qt6", "plugins")

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
