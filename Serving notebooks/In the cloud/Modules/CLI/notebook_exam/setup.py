from setuptools import setup, find_packages

setup(
    name='notebook-exam',
    version='1.0',
    packages=find_packages(),    
    install_requires=[
        'Click',
    	'tabulate==0.8.2',
        'pandas',
        'colorama',
        'pysftp'
    ],
    entry_points={ 'console_scripts': ['notebook-exam=notebook_exam:cli'] },

    package_data={'': ['notebook_commands/scripts/*']},
    include_package_data=True,
)
