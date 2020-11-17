from .check_for_imports import list_files
import subprocess
import psutil
import sys
import os


def call_run_subprocess(file, args=None):
	cmd = [sys.executable, file]
	if args is not None:
		cmd.extend(args)
	process = subprocess.Popen(cmd)

	return process



def run_code(project_dir, entry_point, debug=False):
	files = list_files(project_dir)
	entry_point_file = ''
	
	entry_point_splitted = entry_point.split(".")

	if len(entry_point_splitted) > 1:
		if entry_point_splitted[1] == "py":
			entry_point = f"{entry_point}"
		else:
			entry_point = f"{entry_point_splitted[0]}.py"
	else:
		entry_point = f"{entry_point_splitted[0]}.py"


	for file in files:
		if entry_point in file:
			entry_point_file += file
			break
	if len(entry_point_file) == 0:
		print("Invalid entry point")
		return None

	process = call_run_subprocess(entry_point_file)

	return process


