#!/usr/bin/python
from rfid import ID12LA



reader = ID12LA()
while True:
	tag = reader.wait_for_scan()
	if tag != None:
		print tag
