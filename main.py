from api.check_for_imports import check
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import atexit
import argparse
import os
import time

parser = argparse.ArgumentParser(description='Start a janet project manager')
parser.add_argument('-p', '--project_path',
					nargs='?',
					type=str,
					help='path to your project',
					default=".",
					const=".")

args = parser.parse_args()


project_path = os.path.abspath(args.project_path)


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=check , args = [project_path], trigger="interval", seconds=1)
# scheduler.start()

while True:
	start = time.time()
	check(project_path)
	print(time.time() - start)
	time.sleep(2)

	