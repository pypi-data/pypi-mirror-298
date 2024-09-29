from setuptools import setup, find_packages

setup(
    name='PassSCGui',
    version='0.0.1',
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
    install_requires=[
        'tkinter',  # Tkinter is usually included with Python, but you can specify it here
    ],
)