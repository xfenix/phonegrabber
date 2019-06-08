from setuptools import setup, find_packages


setup(
    name='phone-grabber',
    version='1.0',
    author='Anikin Denis',
    author_email='ad@xfenix.ru',
    packages=find_packages(),
    install_requires = [
        'aiohttp==3.5.4',
        'aiodns==2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'phone-grabber = phonegrabber.main:cli_handler',
        ]
    }
)
