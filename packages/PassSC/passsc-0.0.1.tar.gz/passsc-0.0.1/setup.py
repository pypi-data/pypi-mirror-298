from setuptools import setup, find_packages

setup(
    name='PassSC',
    version='0.0.1',
    author='Babar Ali Jamali',
    author_email='babar995@gmail.com',
    description='CLI Password Strength Checker using regex and time-to-crack estimation.',
    url='https://github.com/babaralijamali/PassSC',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'PassSC=passsc.PassSC:main',
        ],
    },
    install_requires=[
        # Add any dependencies if necessary
    ],
)
