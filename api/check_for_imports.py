import os
import importlib
import subprocess
import sys
import time

from api.db_functions import it_exists, store_last_modified, get_last_modified_time, get_last_modified

def list_files(startpath):
	file_list = []
	env_name = sys.executable.split('/')[-3]
	for root, dirs, files in os.walk(startpath):
		if "/" in root:
			dir_name = root.split("/")[1]
			if dir_name.startswith("."):
				continue
			elif env_name in root:
				continue
  			#REMOVE LATER
			if "api" in root:
				continue
		for f in files:
			if f.endswith(".py") :
				file_list.append(f"{root}/{f}")

	return file_list

def install(packages):
	cmd = [sys.executable, "-m", "pip", "install"]
	cmd.extend(packages)
	subprocess.check_call(cmd)

def check(project_dir):
	files = list_files(project_dir)
	modules = []

	for file in files:
		exists = it_exists(file)

		if not exists:
			store_last_modified(file)
		else:
			last_modified = get_last_modified_time(file)

			if last_modified > get_last_modified(file):
				store_last_modified(file)

				code = open(file, "r")
				lines = code.readlines()
				for line in lines:
					if ("import" in line) and (not line.startswith('#')):
						module = line.split(" ")[1]
						module = module.split(".")[0]
						module = module.rstrip("\n")
						modules.append(module)


	uninstalled_modules = []

	

	for module in modules:
		if module in os.listdir(project_dir):
			print(f"{module} is a local import")
		else:
			try:
				_ = importlib.import_module(module)
				print(f"imported {module} successfully!")
			except Exception as e:
				uninstalled_modules.append(module)
				print(f"could not find {module}")

	

	if len(uninstalled_modules):
		install(uninstalled_modules)



