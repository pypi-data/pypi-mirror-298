from setuptools import setup

setup(
    name='bilkent_traffic',
    version='0.5',
    py_modules=['bilkent_traffic'],
    install_requires=[
        'pyfiglet',
        'pillow',
    ],
    entry_points='''
        [console_scripts]
        bilkent_traffic=bilkent_traffic:main
    ''',
)
