from api.check_for_imports import check
from api.cli_utils import print_header, command

from api.janet_record import JanetRecord

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

janetrecord = JanetRecord(project_path)


scheduler = BackgroundScheduler()
scheduler.add_job(func=check , args=[project_path, janetrecord], trigger="interval", seconds=2)
scheduler.add_job(func=janetrecord.save_janetrecord, trigger="interval", seconds=60)
## kill the scheduled process when janet shutsdown
atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
	process = None
	print_header()
	scheduler.start()

	while True:
		cmd = input(Fore.WHITE+'>>> ')
		process, entry_point = command(cmd, process, entry_point, project_path)

	