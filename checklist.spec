# -*- mode: python ; coding: utf-8 -*-

import os

a = Analysis(
    ['checklist.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('checklist.png', '.'),
        ('checklist.ico', '.'),
        ('close_white.png', '.'),
        ('close_black.png', '.'),
        ('restore_white.png', '.'),
        ('restore_black.png', '.'),
        ('maximize_white.png', '.'),
        ('maximize_black.png', '.'),
        ('minimize_white.png', '.'),
        ('minimize_black.png', '.'),
    ],
    hiddenimports=[
        'win32gui',
        'win32con',
        'win32api',
        'win32ui',
        'win32com.shell.shell',
        'win32com.shell.shellcon',
        'ctypes',
        'tkinter',
        'tkinter.filedialog',
    ],
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
    icon=os.path.abspath('checklist.ico'),
)
