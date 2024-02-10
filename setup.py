from setuptools import setup, find_packages

setup(
    name='ncafe_downloader',
    version='1.1.3',
    packages=find_packages(),
    url='https://github.com/gusfot',
    license='free',
    author='hyunlae',
    author_email='gusfot@gmail.com',
    description='naver_cafe downloader',
    install_requires=[
        'certifi==2024.2.2',
        'chardet==3.0.4',
        'click==8.0.0',
        'idna==2.10',
        'requests==2.31.0',
        'urllib3==1.26'
    ],
    entry_points={
        'console_scripts': [
            'ncafe=naver_cafe.ncafe:cli',
        ],
    },
)
