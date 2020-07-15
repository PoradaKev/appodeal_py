from setuptools import setup

setup(
    name='appodeal_py',
    version='0.1.0',
    description='Appodeal API Client which allows to extract data to Pandas DF',
    author='Oleksandr Korshun',
    author_email='korshunatk@gmail.com',
    url='https://github.com/PoradaKev/appodeal_py',
    packages=[
        'appodeal',
    ],
    license='MIT',
    install_requires=[
        'requests',
        'furl',
        'pandas',
        'tqdm'
    ],
)
