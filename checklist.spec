# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['checklist.py'],
    pathex=[],
    binaries=[],
    datas=[('checklist.png', '.'), ('close_black.png', '.'), ('close_white.png', '.'), ('maximize_black.png', '.'), ('maximize_white.png', '.'), ('minimize_white.png', '.'), ('minimize-black.png', '.'), ('restore_black.png', '.'), ('restore_white.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='checklist',
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
    icon=['checklist.ico'],
)
