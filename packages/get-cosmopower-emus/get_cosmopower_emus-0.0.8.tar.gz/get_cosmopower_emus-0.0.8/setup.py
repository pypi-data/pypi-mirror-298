from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""


    def run(self):
        # Run the standard install first
        print("Running standard install")
        install.run(self)

# Read the README file for the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="get_cosmopower_emus",  # This is the name of your package
    version="0.0.8",  # Package version

    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },

    include_package_data=True,
)
