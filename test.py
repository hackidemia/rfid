#!/usr/bin/python
from rfid import ID12LA

# registered users
people = {"6F005CC7B1": {"name": "stefania", "present": False},
	  "6F005CAB56": {"name": "silver", "present": False}}

# registered inventory
inventory = {"6F005CB5D5": {"name": "RFID kit", "present": True},
	     "6F005C8869": {"name": "Lilypad kit", "present": True},
	     "6F005CC0FB": {"name": "Fritzing kit", "present": True}}

# initialize reader
reader = ID12LA()

while True:
	# wait for a scan
	tag = reader.wait_for_scan()
	# when tag corresponds to a user
	if tag in people:
		# when the user is logged in
		if people[tag]["present"]:
			people[tag]["present"] = False
			print "Safe trip home", people[tag]["name"]
		# when the user is logged out
		else:
			people[tag]["present"] = True
			print "Welcome to the camp", people[tag]["name"]
	# when the tag corresponds to a inventory item
	elif tag in inventory:
		# when the inventory item is not borrowed
		if inventory[tag]["present"]:
			print "To borrow", inventory[tag]["name"], "show your ID tag"
			person = reader.wait_for_scan()
			if person in people:
				inventory[tag]["present"] = False
				print "Thank you", people[person]["name"]
			else:
				print "Sorry, you are not authorized"
		# when the inventory item is borrowed
		else:
			print "To bring back", inventory[tag]["name"], "show your ID tag"
			person = reader.wait_for_scan()
			if person in people:
				inventory[tag]["present"] = True
				print "Thank you", people[person]["name"]
			else:
				print "Sorry, you are not authorized"
	# when the tag is not registered
	else:
		print "Unknown tag :", tag
