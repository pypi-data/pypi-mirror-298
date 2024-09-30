# setup.py

from setuptools import setup

import cfgr

setup(
    name="hyper-bot",
    version=cfgr.VERSION,
    description="The universal config file manager for python",
    author="Harcic",
    author_email="harcic@outlook.com",
    url="https://github.com/HarcicYang/UConfigManager",
    packages=["cfgr"],
    include_package_data=True,
)
