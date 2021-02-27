# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

hidden_imports = [
    'pygubu.builder.tkstdwidgets',
    'pygubu.builder.ttkstdwidgets',
    'pygubu.builder.widgets.dialog',
    'pygubu.builder.widgets.editabletreeview',
    'pygubu.builder.widgets.scrollbarhelper',
    'pygubu.builder.widgets.scrolledframe',
    'pygubu.builder.widgets.tkscrollbarhelper',
    'pygubu.builder.widgets.tkscrolledframe',
    'pygubu.builder.widgets.pathchooserinput',
]

data_files = [
    ('interface.ui', '.'),
    ('hhh1.png', 'imgs'),
]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\yahya\\PycharmProjects\\cna'],
             binaries=[('interface.ui', '.')],
             datas=data_files,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='C:/Users/yahya/PycharmProjects/cna/hhh1.ico',
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
