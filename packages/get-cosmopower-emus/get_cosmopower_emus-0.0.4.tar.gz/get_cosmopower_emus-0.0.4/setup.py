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

        # Now run the custom post-install command
        try:
            # Use subprocess to ensure it runs correctly
            subprocess.check_call([os.sys.executable, "-m", "get_cosmopower_emus.get_cosmopower_emus"])
        except subprocess.CalledProcessError as e:
            print(f"Error during post-installation: {e}")
        else:
            print("Successfully ran get_cosmopower_emus.get_cosmopower_emus")


# Read the README file for the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="get_cosmopower_emus",  # This is the name of your package
    version="0.0.4",  # Package version

    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'get_cosmopower_emus = get_cosmopower_emus.get_cosmopower_emus:main',
        ],
    },

    include_package_data=True,
)
