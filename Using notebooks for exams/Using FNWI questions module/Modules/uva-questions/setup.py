from setuptools import setup

setup(
    name='uva-questions',
    version='1.0',
    description='UvA questions module',
    packages=['questions'],
    url='https://github.com/jessesar/uva-questions',
    author='Jesse van der Sar',
    author_email='j.d.vandersar@uva.nl',
    install_requires=[
        'ipywidgets==7.0.5',
        'jupyter==1.0.0',
        'ipython==5.1.0',
        'requests'
    ],
)
