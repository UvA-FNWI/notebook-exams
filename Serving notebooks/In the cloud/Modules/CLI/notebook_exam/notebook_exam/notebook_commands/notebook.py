import click
import sys
import os
import subprocess

from colorama import Fore, Back, Style

@click.command('start')
def start():
    '''Start the Docker notebook environment.'''

    script_path = os.path.dirname(os.path.realpath(__file__)) +'/scripts/run-notebook.sh'
    proc = subprocess.Popen([script_path], shell=False)
    proc.communicate()