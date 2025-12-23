from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all
import os

block_cipher = None

# docx 依然建议使用 collect_all，因为它比较小且依赖复杂
docx_tmp_ret = collect_all('docx')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=docx_tmp_ret[1],
    datas=docx_tmp_ret[0],
    hiddenimports=docx_tmp_ret[2] + [
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        'reportlab',
        'core.presets',
        'core.math_engine',
        'ui.main_window',
        'ui.preview_canvas',
        'services.pdf_exporter',
        'services.word_exporter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'test'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MathGenius',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/icon.ico'] if os.path.exists('resources/icon.ico') else None,
)

app = BUNDLE(
    exe,
    name='MathGenius.app',
    icon='resources/icon.icns' if os.path.exists('resources/icon.icns') else None,
    bundle_identifier='com.mathgenius.generator',
)
