from setuptools import setup, find_packages

setup(
    name='binance-archiver',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'aiofiles',
        'websockets',
        'azure-storage-blob',
        'python-dotenv',
        'aiohttp',
        'requests',
        'websocket',
        'python-dotenv',
        'websockets',
        'requests',
        'websocket',
        'websocket-client',
        'orjson'
    ],
    author="Daniel Lasota",
    author_email="grossmann.root@gmail.com",
    description="A package for archiving Binance data",
    keywords="binance archiver quant data sprzedam opla",
    url="http://youtube.com",
    python_requires='>=3.11',
)
