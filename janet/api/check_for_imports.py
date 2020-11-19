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
		for f in files:
			if f.endswith(".py") :
				file_list.append(f"{root}/{f}")

	return file_list

def update_requirements(janetrecord):
	spit_packages = [sys.executable, "-m", "pip", "freeze"]
	pip_freeze = subprocess.run(spit_packages, universal_newlines=True, stdout=subprocess.PIPE)

	frozen_packages = pip_freeze.stdout
	with open("_temp_janet_file.txt", "w") as temp_file:
		temp_file.write(frozen_packages)

	with open("requirements.txt", "w") as requirements_file:
		for line in open("_temp_janet_file.txt"):
			line_splitted = line.split("==")[0].lower()
			if line_splitted not in janetrecord.janet_requirements:
				requirements_file.writelines(line)

	os.remove("_temp_janet_file.txt")



def install(modules):
	cmd = [sys.executable, "-m", "pip", "install"]
	cmd.extend(modules)
	
	pip_install = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE)
	


def check_module_in_pip(module):
	cmd = [sys.executable, '-m', 'pip', 'search', module]
	result = subprocess.run(cmd, capture_output=True)
	return len(result.stdout) > 0


def resolve_imports(lines):
	modules_to_resolve = []

	for line in lines:
		if( ("import" in line) and
			 (not line.startswith('#')) and 
			 	(not line.endswith("import")) ):
			line_formated = line.replace("import","")
			line_split= line_formated.split(",")

			for imported_module in line_split:
				as_keyword_index = imported_module.find(" as ")
				if as_keyword_index != -1:
					imported_module = imported_module[0:as_keyword_index]
					
				imported_module = imported_module.replace(" ","")
				imported_module = imported_module.split(".")[0]
				imported_module = imported_module.rstrip("\n")
				modules_to_resolve.append(imported_module)

	return modules_to_resolve



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
				
				modules_to_resolve = resolve_imports(lines)

				if len(modules_to_resolve):
					modules.extend(modules_to_resolve)


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

	update_requirements(janetrecord)



