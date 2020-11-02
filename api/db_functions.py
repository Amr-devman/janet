from datetime import datetime, timedelta, date, timezone
import redis
import os


def get_last_modified_time(filepath):
	unix_epoch = os.path.getmtime(filepath)
	return unix_epoch

def create_cnxn(host='localhsot', port=6369):
	r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
	return r

def store_last_modified(filepath):
	last_modified = get_last_modified_time(filepath)
	r = create_cnxn()
	r.set(filepath, last_modified)

def get_last_modified(filepath):
	r = create_cnxn()
	return float(r.get(filepath))

def it_exists(filepath):
	r = create_cnxn()
	exist = r.exists(filepath)
	return exist


	
