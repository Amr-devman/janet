from api.check_for_imports import check

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import atexit

from colorama import Fore
import argparse
import os
import time
import logging

logging.getLogger('apscheduler.scheduler').setLevel('ERROR')
logging.getLogger('apscheduler.executors.default').propagate = False

parser = argparse.ArgumentParser(description='Start a janet project manager')
parser.add_argument('-p', '--project_path',
					nargs='?',
					type=str,
					help='path to your project',
					default=".",
					const=".")


parser.add_argument('-s', '--script',
					nargs='?',
					type=str,
					help='specify the entry point for your project',
					default="",
					const="")

args = parser.parse_args()
project_path = os.path.abspath(args.project_path)


scheduler = BackgroundScheduler()
scheduler.add_job(func=check , args=[project_path], trigger="interval", seconds=2)



def print_header():
    print(Fore.WHITE + 'Starting Janet...')
    print(Fore.GREEN + 'Janet is running, use the command line to issue commands like:')
    print(Fore.RED+ '	1. run-code')
    print(Fore.RED+ '	2. run-and-debug-code')
    print(Fore.WHITE)

def command(command):
	if command.lower() == 'exit':
		exit()
	elif command.lower() == 'run-code':
		pass
	elif command.lower() == 'run-and-debug-code':
		pass



if __name__ == "__main__":
	print_header()
	scheduler.start()
	while True:
		cmd = input(Fore.WHITE+'> ')
		command(cmd)

	