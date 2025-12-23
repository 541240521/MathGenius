from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all

block_cipher = None

# 使用 collect_all 彻底抓取 PyQt6 和 docx 的所有依赖
docx_tmp_ret = collect_all('docx')
pyqt6_tmp_ret = collect_all('PyQt6')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=docx_tmp_ret[1] + pyqt6_tmp_ret[1],
    datas=docx_tmp_ret[0] + pyqt6_tmp_ret[0],
    hiddenimports=docx_tmp_ret[2] + pyqt6_tmp_ret[2] + [
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
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MathGenius',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/icon.ico'] if os.path.exists('resources/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MathGenius',
)

app = BUNDLE(
    coll,
    name='MathGenius.app',
    icon='resources/icon.icns' if os.path.exists('resources/icon.icns') else None,
    bundle_identifier='com.mathgenius.generator',
)
