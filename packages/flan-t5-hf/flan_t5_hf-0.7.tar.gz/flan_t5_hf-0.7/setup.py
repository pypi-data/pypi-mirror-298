from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
import os
import sys
from pip._internal import main as pip_main

def install_package(package):
    pip_main(['install', package])

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # Call the original install command
        install.run(self)
        from flan_t5_hf.text_generator import download_model_if_needed, get_model_directory
        if not os.getenv('PACKAGE_BUILDING', '0') == '1':

            model_dir = get_model_directory()
            download_model_if_needed(model_dir)

class PostDevelopCommand(develop):
    """Post-installation for installation mode."""

    def run(self):
        # Call the original install command
        develop.run(self)
        if not os.getenv('PACKAGE_BUILDING', '0') == '1':
            from flan_t5_hf.text_generator import download_model_if_needed, get_model_directory
            model_dir = get_model_directory()
            download_model_if_needed(model_dir)

class PostEggInfoCommand(egg_info):
    """Post-installation for installation mode."""

    def run(self):
        # Call the original install command
        egg_info.run(self)
        if not os.getenv('PACKAGE_BUILDING', '0') == '1':
            from flan_t5_hf.text_generator import download_model_if_needed, get_model_directory
            model_dir = get_model_directory()
            download_model_if_needed(model_dir)


setup(
    name="flan_t5_hf",
    version="0.7",
    packages=find_packages(),
    install_requires=[],
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
        'egg_info': PostEggInfoCommand
    },
    include_package_data=True,
    package_data={
        "flan_t5_hf": [],
    },
)
