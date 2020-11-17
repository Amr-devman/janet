import os
import importlib
import subprocess
from subprocess import Popen, PIPE
import sys
import time


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

def install(modules):
	cmd = [sys.executable, "-m", "pip", "install"]
	spit_requirements_txt = [sys.executable, "-m", "pip", "freeze"]
	requirements_file = open("requirements.txt", "w")
	cmd.extend(modules)
	
	process_1 = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE)
	process_2 = subprocess.run(spit_requirements_txt, universal_newlines=True, input=process_1.stdout, stdout=requirements_file)



def check_module_in_pip(module):
	cmd = [sys.executable, '-m', 'pip', 'search', module]
	result = subprocess.run(cmd, capture_output=True)
	return len(result.stdout) > 0



def check(project_dir, janetrecord):
	files = list_files(project_dir)
	modules = []

	for file in files:
		exists = janetrecord.it_exists(file)

		if not exists:
			janetrecord.store_last_modified(file)
		else:
			last_modified = janetrecord.get_last_modified_time(file)

			if last_modified > janetrecord.get_last_modified_from_records(file):
				janetrecord.store_last_modified(file)

				code = open(file, "r")
				lines = code.readlines()
				for line in lines:
					if( ("import" in line) and
						 (not line.startswith('#')) and 
						 	(not line.endswith("import")) ):
						module = line.split(" ")[1]
						module = module.split(".")[0]
						module = module.rstrip("\n")
						modules.append(module)


	uninstalled_modules = []

	

	for module in modules:
		
		if (module == " ") or (module == ""):
			continue
		elif module in os.listdir(project_dir):
				continue


		found = importlib.find_loader(module)
		if not found:
			is_in_pip = check_module_in_pip(module)
			if not is_in_pip:
				print(f"{module} is neither a local import nor a pip package, skipping ...")
				continue
			else:
				uninstalled_modules.append(module)
			

	

	if len(uninstalled_modules):
		print('You have the following uninstalled module(s)')
		for idx, mod in enumerate(uninstalled_modules):
			print(f"	{idx}: {mod}")
		print("I'll take care of it!")
		print()
 
		install(uninstalled_modules)	
		print()
		print("Installation completed")
		print("press enter to show cli..")


