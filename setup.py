from setuptools import setup

setup(
    name='ncafe_downloader',
    version='1.1',
    packages=[],
    url='https://github.com/gusfot',
    license='free',
    author='hyunlae',
    author_email='gusfot@gmail.com',
    description='ncafe downloader',
    install_requires=[
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'click==8.0.0',
        'idna==2.10',
        'requests==2.26',
        'urllib3==1.26'
    ],
    entry_points={
    'console_scripts': [
        'ncafe = ncafe:main',
    ],
    },
)