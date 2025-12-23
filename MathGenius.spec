from PyInstaller.utils.hooks import collect_data_files
import os

block_cipher = None

# Collect data files for docx
docx_datas = collect_data_files('docx')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=docx_datas,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'reportlab',
        'docx',
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
    console=False,
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
