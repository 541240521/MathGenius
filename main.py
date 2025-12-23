import sys
import os
import traceback

# 针对 Windows 打包环境的 DLL 路径补丁
if sys.platform == 'win32' and getattr(sys, 'frozen', False):
    import os
    # 获取程序运行目录
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    
    # 强制将所有可能的 DLL 目录加入搜索路径
    possible_paths = [
        base_path,
        os.path.join(base_path, "PyQt6", "Qt6", "bin"),
    ]
    
    for p in possible_paths:
        if os.path.exists(p):
            try:
                os.add_dll_directory(p)
            except Exception:
                pass

    # 设置插件路径
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(base_path, "PyQt6", "Qt6", "plugins")

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MathGenius PRO")
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
