from api.check_for_imports import check
from api.run import run_code

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import atexit

from colorama import Fore
import argparse
import os
import time
import logging
import signal

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
entry_point = args.script




scheduler = BackgroundScheduler()
scheduler.add_job(func=check , args=[project_path], trigger="interval", seconds=2)
## kill the scheduled process when janet shutsdown
atexit.register(lambda: scheduler.shutdown())



def print_header():
    print(Fore.WHITE + 'Starting Janet...')
    print(Fore.GREEN + 'Janet is running, use the command line to issue commands like:')
    print(Fore.RED+ '	1. run-code (to run code from the selected entry point')
    print(Fore.RED+ '	2. change-entrypoint (change the entry point')
    print(Fore.RED+ '	3. kill (to end a run)')
    print(Fore.RED+ '	4. kill-server (special command for if your code runs a server)')
    print(Fore.RED+ '	5. exit (to stop janet)')
    print(Fore.WHITE)

def command(command, process):
	global entry_point

	command = command.replace(" ", "")

	if command.lower() == 'exit':
		if process is not None:
			process.send_signal(signal.SIGINT)
		exit()
		
	elif command.lower() == 'run-code':
		if process is not None:
			print("you have to kill the current process before starting a new one")
		else:
			process = run_code(project_path, entry_point, debug=False)
		return process

	elif command.lower() == 'change-entrypoint':
		new_entry_point = ''
		while len(new_entry_point) == 0:
			new_entry_point = input(Fore.WHITE+'New entry point ? ')
			new_entry_point = new_entry_point.replace(" ","")
		entry_point = new_entry_point

		return process
	elif command.lower() == 'kill':
		if process is not None:
			process.kill()
		else:
			print("Nothing to kill")

		return None

	elif command.lower() == 'kill-server':
		if process is not None:
			process.send_signal(signal.SIGINT)
		else:
			print("Nothing to kill")

		return None


	else:
		return process


if __name__ == "__main__":
	process = None
	print_header()
	scheduler.start()
	while True:
		cmd = input(Fore.WHITE+'>>> ')
		process = command(cmd, process)

	