from setuptools import setup, find_packages

setup(
    name='notebook_exam',
    version='0.1',
    py_modules=['notebook-exam'],    
    install_requires=[
        'Click',
    	'tabulate',
	'pandas',
	'colorama'
    ],
    entry_points='''
        [console_scripts]
        notebook-exam=cli:cli
    ''',
)
