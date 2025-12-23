import sys
import os
import traceback

# 针对 Windows 打包环境的 DLL 路径补丁
try:
    if sys.platform == 'win32' and getattr(sys, 'frozen', False):
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

    from PyQt6.QtWidgets import QApplication, QMessageBox
    from ui.main_window import MainWindow

except Exception as e:
    # 如果加载失败，尝试用 Windows 原生弹窗显示错误
    error_msg = f"程序启动失败!\n\n错误类型: {type(e).__name__}\n错误信息: {str(e)}\n\n堆栈追踪:\n{traceback.format_exc()}"
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, error_msg, "启动错误", 0x10)
    else:
        print(error_msg)
    sys.exit(1)

def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("MathGenius PRO")
        app.setStyle("Fusion")
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        error_msg = f"运行过程中出错:\n{traceback.format_exc()}"
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, error_msg, "运行错误", 0x10)
        else:
            print(error_msg)

if __name__ == "__main__":
    main()
