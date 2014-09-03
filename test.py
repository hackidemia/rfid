#!/usr/bin/python

import sys
from rfid import ID12LA
from datetime import date
from PyQt4.QtGui import *
from PyQt4.QtCore import *


# registered users
people = {"----------": {"name": "kati", "present": "False"},
	  "----------": {"name": "mati", "present": "False"}}

# registered inventory
inventory = {"----------": {"name": "Sensor kit", "present": "True", "date": "--.--", "user": "----"},
	     "----------": {"name": "Lilypad kit", "present": "True", "date": "--.--", "user": "----"},
	     "----------": {"name": "Fritzing kit", "present": "True", "date": "--.--", "user": "----"}}

class MyGrid(QGridLayout):
    def __init__(self, *args):
        QGridLayout.__init__(self, *args)
        
	self.table = QTableWidget(3, 4)
	self.label = QLabel("Welcome to makercamp inventory")

        self.thread = RevolveThread()
	self.connect(self.thread, SIGNAL('setmydata()'), self.setmydata)
	self.connect(self.thread, SIGNAL('setmytext(QString)'), self.setmytext)
	self.thread.start()
	
	self.setmydata()
	
	self.addWidget(self.label, 0, 0)
	self.addWidget(self.table, 1, 0)

    def setmytext(self, text):
      self.label.setText(text)

    def setmydata(self):
	row = 0
	col = 0
        horHeaders = ["date", "name", "present", "user"]
        for key in inventory:
	    for header in inventory[key]:
		newitem = QTableWidgetItem(inventory[key][header])
		self.table.setItem(row, col, newitem)
		#print inventory[key][header]
		col += 1
	    col = 0
	    row += 1
        self.table.setHorizontalHeaderLabels(horHeaders)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

class RevolveThread(QThread):
    def __init__(self):
        super(RevolveThread , self).__init__()

    def run(self):
	# initialize reader
	reader = ID12LA()
	while True:
	    # wait for a scan
	    tag = reader.wait_for_scan()
	    # when tag corresponds to a user
	    if tag in people:
		    # when the user is logged in
		    if people[tag]["present"] == "True":
			    people[tag]["present"] = "False"
			    print "Safe trip home", people[tag]["name"]
			    self.emit(SIGNAL('setmytext(QString)'), "Safe trip home " + people[tag]["name"])
		    # when the user is logged out
		    else:
			    people[tag]["present"] = "True"
			    print "Welcome to the camp", people[tag]["name"]
			    self.emit(SIGNAL('setmytext(QString)'), "Welcome to the camp " + people[tag]["name"])
	    # when the tag corresponds to a inventory item
	    elif tag in inventory:
		    # when the inventory item is not borrowed
		    if inventory[tag]["present"] == "True":
			    print "To borrow", inventory[tag]["name"], "show your ID tag"
			    self.emit(SIGNAL('setmytext(QString)'), "To borrow " + inventory[tag]["name"] + " show your ID tag")
			    person = reader.wait_for_scan()
			    if person in people:
				    inventory[tag]["present"] = "False"
				    inventory[tag]["date"] = str(date.today())
				    inventory[tag]["user"] = people[person]["name"]
				    print "Thank you", people[person]["name"]
				    self.emit(SIGNAL('setmytext(QString)'), "Thank you " + people[person]["name"])
			    else:
				    print "Sorry, you are not authorized"
				    self.emit(SIGNAL('setmytext(QString)'), "Sorry, you are not authorized")
		    # when the inventory item is borrowed
		    else:
			    print "To bring back", inventory[tag]["name"], "show your ID tag"
			    self.emit(SIGNAL('setmytext(QString)'), "To bring back " + inventory[tag]["name"] + " show your ID tag")
			    person = reader.wait_for_scan()
			    if person in people:
				    inventory[tag]["present"] = "True"
				    inventory[tag]["date"] = str(date.today())
				    inventory[tag]["user"] = people[person]["name"]
				    print "Thank you", people[person]["name"]
				    self.emit(SIGNAL('setmytext(QString)'), "Thank you " + people[person]["name"])
			    else:
				    print "Sorry, you are not authorized"
				    self.emit(SIGNAL('setmytext(QString)'), "Sorry, you are not authorized")
	    # when the tag is not registered
	    else:
		    print "Unknown tag :", tag
		    self.emit(SIGNAL('setmytext(QString)'), "Unknown tag: " + tag)
	    self.emit(SIGNAL('setmydata()'))

def main(args):
    app = QApplication(args)
    window = QMainWindow()
    centralWidget = QWidget()
    
    grid = MyGrid()
    
    window.setCentralWidget(centralWidget)
    centralWidget.setLayout(grid)
    window.resize(400, 300)
    window.setWindowTitle('Makecamp inventory')
    window.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)
