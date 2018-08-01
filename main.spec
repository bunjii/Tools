# -*- mode: python -*-

import requests

requests_base_dir = os.path.dirname(requests.__file__)
requests_tree = Tree(requests_base_dir, prefix='requests')
block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\Users\\92245\\Desktop\\tools07', 'D:\\Users\\92245\\Desktop\\tools07\\solver'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               icon_tree,
               data_tree,
               astropy_tree,requests_tree,
               strip=None,
               upx=True,
               name=vaex.__build_name__)
