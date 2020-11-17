from .run import run_code
from .check_for_imports import install

from colorama import Fore
import argparse
import os
import time
import logging
import signal

from pyfiglet import Figlet



def print_header():
	f = Figlet(font='slant')
	print(f.renderText('JANET'))
	print_cmd()

def print_cmd():
    print(Fore.WHITE + 'Cool stuff you could do:')
    print(Fore.GREEN+ '	1. run (to run the selected entry point (running again will kill the current python process)')
    print(Fore.GREEN+ '	1. install <PACKAGE_1> <PACKAGE_2> ... (install packages manually)')
    print(Fore.GREEN+ '	2. change-entrypoint (change the entry point')
    print(Fore.GREEN+ '	3. kill (to manually end a run)')
    print(Fore.GREEN+ '	4. exit (to stop janet)')
    print(Fore.GREEN+ '	5. menu')
    print(Fore.GREEN+ '	\nUse TAB to autocomplete commands')
    print(Fore.WHITE)




def command(command, process, entry_point, project_path):
	command_no_spaces = command.replace(" ", "")
	command_splited = command.split(" ")

	if command_no_spaces.lower() == 'exit':
		if process is not None:
			process.send_signal(signal.SIGINT)
		exit()

	elif command_splited[0].lower() == "install":
		modules = []
		for arg in command_splited[1:]:
			if (arg == " ") or (arg == ""):
				continue
			else:
				modules.append(arg)
		install(modules)
		return process, entry_point


	elif command_no_spaces.lower() == 'run':
		if process is not None:
			print("you have to kill the current process before starting a new one")
			process.send_signal(signal.SIGINT)

		process = run_code(project_path, entry_point, debug=False)
		return process, entry_point

	elif command_no_spaces.lower() == 'change-entrypoint':
		new_entry_point = ''
		while len(new_entry_point) == 0:
			new_entry_point = input(Fore.WHITE+'New entry point ? ')
			new_entry_point = new_entry_point.replace(" ","")
		entry_point = new_entry_point
		return process, entry_point


	elif command_no_spaces.lower() == 'kill':
		if process is not None:
			process.send_signal(signal.SIGINT)
		else:
			print("Nothing to kill")

		return None, entry_point

	elif command_no_spaces.lower() == 'menu':
		print_cmd()
		return process, entry_point

	else:
		return process, entry_point




		