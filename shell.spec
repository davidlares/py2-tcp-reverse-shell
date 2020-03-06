# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['shell.py'],
             pathex=['Z:\\opt\\projects\\security\\udemy\\master-ethical-hacking-for-python\\reverse-shell\\scripts'],
             binaries=[],
             datas=[('./image.png', 'image.png')],
             hiddenimports=[],
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
          name='shell',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
