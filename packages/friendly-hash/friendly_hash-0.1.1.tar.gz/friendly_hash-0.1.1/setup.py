from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a message after installation."""
    def run(self):
        install.run(self)
        # Custom post-install message
        print("\n\nPlease add \n`export PATH=$PATH:~/.local/bin`\n to your .bashrc or .zshrc\n")


# Read the version number from version.py
version = {}
with open("friendly_hash/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='friendly_hash',
    version=version['__version__'], # Please check ./friendly_hash/version.py
    author='JackyLiu',
    author_email='jjkka132@gmail.com',
    description='A tool to rename files with human-readable hashes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/HTLife/friendly_hash',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'codenamize>=1.2.3'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'friendly_hash=friendly_hash.friendly_hash:main',
        ],
    },
)
