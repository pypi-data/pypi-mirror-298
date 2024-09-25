from distutils.core import setup

setup(name='amz_extractor',
      version='1.0.6',
      description='提取亚马逊详情页和评论信息',
      author='lonely',
      packages=['amz_extractor'],
      package_dir={'amz_extractor': 'amz_extractor'},
      install_requires=['dateparser>=1.1.4', 'pyquery>=1.4.3']
      )

"""
# 更新版本命令

python setup.py sdist bdist_wheel

twine upload dist/*

pypi-AgEIcHlwaS5vcmcCJGZlNThkN2JmLTczY2YtNDFmNC05NzM5LWE4N2ZkZjkxZGJmNAACKlszLCJiYWRlYjNjMS1lNDE2LTQ2MzEtYjYyMy1lNGIwZTFiNzYyNTYiXQAABiCxA9Q6zYnY8Glrouk95tjoz_LRmVbl_GWE4tcen0pTyA
"""