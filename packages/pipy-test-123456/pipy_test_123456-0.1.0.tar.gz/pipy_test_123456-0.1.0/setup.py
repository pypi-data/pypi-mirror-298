from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='pipy_test_123456',    # 包名
      version='0.1.0',        # 版本号
      description='test pip upload',
      long_description=long_description,
      author='xp',
      author_email='1426813058@qq.com',
      url='',
      install_requires=[],	# 依赖包会同时被安装
      license='MIT',
      packages=find_packages())
