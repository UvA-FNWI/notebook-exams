import click
import subprocess
import os

@click.command('cluster')
@click.argument('NUMBER_OF_WORKERS')
@click.argument('WORKER_FLAVOR')
def cluster(number_of_workers, worker_flavor):
	script_path = os.path.dirname(os.path.realpath(__file__)) +'/scripts/setup-cluster.sh'
	proc = subprocess.Popen([script_path, number_of_workers, worker_flavor], shell=False)
	proc.communicate()