from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstall(install):
    def run(self):
        # Check for tkinter
        os.system('python -m passscgui.tkinter_check')
        install.run(self)

setup(
    name='PassSCGui',
    version='0.0.2',
    author='Babar Ali Jamali',
    author_email='babar995@gmail.com',
    description='GUI Password Strength Checker using regex and time-to-crack estimation.',
    url='https://github.com/babaralijamali/PassSCGui',
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'PassSCGui=passscgui.PassSCGui:main',
        ],
    },
    cmdclass={
        'install': CustomInstall,
    },
)
