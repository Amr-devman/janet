import json
import os
from datetime import datetime

class JanetRecord:
	def __init__(self, project_dir):
		self.project_dir = project_dir

		janetrecord_exists = self.check_for_existing_records()

		if janetrecord_exists:
			self.janetrecord = self.load_janetrecord()
		else:
			self.janetrecord = self.create_janetrecord()
			self.save_janetrecord()
		
		self.add_to_gitignore()


	def check_for_existing_records(self):
		project_files = os.listdir(self.project_dir)

		return ".janetrecord.json" in project_files

	def create_janetrecord(self):
		curr_time = datetime.now()
		curr_time = curr_time.strftime("%m/%d/%Y, %H:%M:%S")
		janetrecord = 	{
							"_project_dir": self.project_dir,
							"_creation_time": curr_time,
							"records": {}
						}
		return janetrecord


	def save_janetrecord(self):
		janetrecord_filepath = os.path.join(self.project_dir, ".janetrecord.json")
		with open(janetrecord_filepath, 'w') as f:
			json.dump(self.janetrecord, f, indent=4, sort_keys=True)


	def load_janetrecord(self):
		janetrecord_filepath = os.path.join(self.project_dir, ".janetrecord.json")
		with open(janetrecord_filepath) as f:
			janetrecord = json.load(f)
		return janetrecord

	def add_to_gitignore(self):
		project_files = os.listdir(self.project_dir)

		if ".gitignore" in project_files:
			gitignore_path = os.path.join(self.project_dir, ".gitignore")
			with open(gitignore_path, "a") as gitignore:
				gitignore.write("\n#janet records\n.janetrecord.json")
		else:
			print("Did not find a gitignore")
			print("use git init and run janet again or add it to .gitignore manually!")


	def get_last_modified_time(self, filepath):
		unix_epoch = os.path.getmtime(filepath)
		return unix_epoch

	def store_last_modified(self, filepath):
		last_modified = self.get_last_modified_time(filepath)
		self.janetrecord["records"][filepath] = last_modified


	def get_last_modified_from_records(self, filepath):
		try:
			last_modified = self.janetrecord["records"][filepath] 
		except:
			last_modified = None
		
		return last_modified

	def it_exists(self, filepath):
		try:
			last_modified = self.janetrecord["records"][filepath]
			exists = True 
		except:
			exists = False
		
		return exists
