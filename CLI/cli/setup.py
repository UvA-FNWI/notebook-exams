from setuptools import setup

setup(
    name='notebook-exam',
    version='0.1',
    py_modules=['notebook-exam'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        notebook-exam=cli:cli
    ''',
)