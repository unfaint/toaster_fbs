# -*- mode: python -*-

block_cipher = None


a = Analysis(['/home/kruglov/projects/toaster_fbs/src/main/python/main.py'],
             pathex=['/home/kruglov/projects/toaster_fbs/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/home/kruglov/projects/toaster_fbs/venv/lib/python3.6/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/home/kruglov/projects/toaster_fbs/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Toaster',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Toaster')
