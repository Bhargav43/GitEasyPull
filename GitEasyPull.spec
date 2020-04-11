# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['GitEasyPull.py'],
             pathex=['H:\\Projects\\Python Related Stuff\\Pyzo Projects\\GitEasyPull'],
             binaries=[],
             datas=[],
             hiddenimports=['os', 'time', 'shutil', 'sys', 'stat', 'subprocess', 'requests'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GitEasyPull',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='H:\\Projects\\Python Related Stuff\\Pyzo Projects\\GitEasyPull\\Gitpull-icon.ico')
