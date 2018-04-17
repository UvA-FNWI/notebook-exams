from setuptools import setup, find_packages

setup(
    name='uva-notebook',
    version='1.0',
    description = 'CLI tool for starting UvA notebook environment.',
    author = 'Jesse van der Sar',
    author_email = 'j.d.vandersar@uva.nl',
    
    packages=find_packages(),    
    install_requires=[
        'Click',
        'colorama',
    ],
    entry_points={ 'console_scripts': ['uva-notebook=uva_notebook:cli'] },

    package_data={'': ['scripts/*']},
    include_package_data=True,
)
