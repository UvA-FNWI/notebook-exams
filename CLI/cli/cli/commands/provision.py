import click
import subprocess
import os

@click.command('cluster')
@click.argument('NUMBER_OF_WORKERS', default='5')
@click.argument('WORKER_FLAVOR', default='n1-standard-1')
def cluster(number_of_workers, worker_flavor):
	script_path = os.path.dirname(os.path.realpath(__file__)) +'/setup-cluster.sh'
	proc = subprocess.Popen([script_path, number_of_workers, worker_flavor], shell=False)
	proc.communicate()