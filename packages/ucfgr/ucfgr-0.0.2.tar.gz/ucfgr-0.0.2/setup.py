# setup.py

from setuptools import setup

import cfgr

setup(
    name="ucfgr",
    version=cfgr.VERSION,
    description="The universal config file manager for python",
    author="Harcic",
    author_email="harcic@outlook.com",
    url="https://github.com/HarcicYang/UConfigManager",
    packages=["cfgr", "cfgr.utils"],
    include_package_data=True,
)
