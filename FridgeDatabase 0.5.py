from datetime import datetime
import os
import pickle
import array
import numpy
import csv
#Written by Kenny Ma. Keep it simple stupid. 

#Directories and paths.  
# dataPath = "\\C:\\Users\\Kenny Ma\\Desktop\\TEST\\"
# dataPath = "C:\\Users\\MaK23074\\Desktop\\TEST\\FRIDGE_DATABASE.txt"
# dataPath = "C:\\Users\\MaK23074\\Desktop\\TEST\\test.txt"
dataPath = "Z:\\For Kenny\\FRIDGE_DATABASE\\FRIDGE_DATABASE.txt"
exportPath = "Z:\\For Kenny\\FRIDGE_DATABASE\\DBExport"

#Global Variables and Pointers
main = True
labDB = []
pFileName = dataPath

# Classes and Inheritance
#Example of Shelf Label FG001_R1 = Fridge 001 Frist Right Shelf from Top

class LaboratoryStorage:
	def __init__ (self):
		self.DB = []

	def addItem(self, item):

		self.DB.append(item)

	def searchItem(self, itemName):
		for each in self.DB:
			if each.name == itemName:
				return each.index
		return None

class storageShelf:
	def __init__ (self, shelfLabel):
		self.shelfLabel = shelfLabel
		self.storedItems = []

	def name(self):
		return self.shelfLabel

	def returnShelves(self):
		return self.shelves

	def searchItem(self, item):
		index = 0
		for each in self.storedItems:
			if item.name == each.name:
				return index
		return None

	def storeItem(self, item):
		self.storedItems.append(item)

	def removeItem(self, item):
		self.storedItems.append(item)

class item:
	def __init__ (self, barcode, shelf, operator):
		self.status = "Available"
		self.name = barcode 
		self.shelf = shelf
		self.history  = []
		self.history.append(("STORED", shelf, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), operator))

	def plateLogs(self):
		return self.history

	def movePlate(self, newShelf, operator):
		self.shelf = newShelf
		self.history.append(("MOVED", newShelf, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), operator))

	def disposePlate(self, newShelf, operator):
		self.shelf = None
		self.status = "Unavailable"
		self.history.append(("DISPOSED", shelf, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), operator))

#Database Data Structures

#Data Persistance Loading and Saving methods
def saveDatabase():
	with open(pFileName, "wb") as fp:   #Pickling
		pickle.dump(labDB, fp)

def loadDatabase():
	with open(pFileName, "rb") as fp:   #Unpickling
		return pickle.load(fp)

def backupDatabase():
	backupName = pFileName.removesuffix(".txt") + datetime.now().strftime("BACKUP_%d_%m_%Y_%H_%M.p")
	with open(backupName, "wb") as fp:   #Pickling
		pickle.dump(labDB, fp)

#Intepreter helper functions

def printDBBarcodes():
	barcodes = []
	for each in labDB:
		print(each.name, each.shelf)

def printAllDB():
	listOfShelves = []
	for each in labDB:
		listOfShelves.append(each.shelf)

	listOfShelves = list(set(listOfShelves))
	listOfShelves.sort()
	dbArray = []
	for each in listOfShelves:
		dbArray.append([each])

	for eachItem in labDB:
		for eachShelf in dbArray:
			if eachShelf[0] == eachItem.shelf:
				eachShelf.append(eachItem.name)

	file = open(exportPath + datetime.now().strftime("_%d_%m_%Y_%H_%M.csv"), 'w+', newline ='') 
	with file:
		write = csv.writer(file) 
		write.writerows(dbArray) 
	print("Successfully exported CSV to " + exportPath )

def bulkMovePlates(barcodes, newShelf, operator):
	for each in barcodes:
		searchResult = barcodeSearch(each)
		if searchResult != False:
			searchResult.movePlate(newShelf, operator)
		else:
			labDB.append(item(each,newShelf,operator))
	saveDatabase()
	backupDatabase()
	print("Successfully moved plates")
	return 

def logHistory(barcode):
	returndatetime.now()


def bulkScanBarcodes():
		print("Enter 'done' when complete")
		barcodeStack =  []
		complete = False
		while not complete: 
			barcode = input("Scan barcode:")
			if barcode == "":
				pass 
			elif barcode == "done" or command =="d":
				stack = list(set(barcodeStack))
				number = len(stack)
				print("Number of plates scanned :" + str(number))
				return stack
			else:
				barcodeStack.append(barcode)

# def resetDB():
# 	labDB = []
# 	saveDatabase()

#Search Engine

def search():
	complete = False
	searchStack = []
	print("Enter 'done' when complete")
	while not complete:
		
		entry = input("Enter Plate Barcodes:")
		if entry == "done" or command =="d":
			stackPrintLocation(bulkBarcodeSearch(searchStack))
			complete = True
		else:
			searchStack.append(entry)

def barcodeSearch(barcode):
	for each in labDB:
		if each.name == barcode:
			return each
	return False

def bulkBarcodeSearch(searchStack):
	found = []
	for each in searchStack:

		query = barcodeSearch(each)
		if query == False:
			found.append([each, "Not Found"])
			
		else:
			found.append([each, query])
		
	return found

def stackPrintLocation(searchStack):
	for each in searchStack:
		if each[1] == "Not Found":
			print(each[0]  + " Not Found")
		else:
			print(each[0] +" in " + each[1].shelf)


#Intepreter Commands
def checkIn():
	complete = False
	while not complete:
		operator = input("Enter Operator:")
		shelf = input("Scan Fridge Shelf:")
		confirm = input("Operator: " + operator + "   Target shelf: " + shelf  + "\n Is this correct?(Y/N/exit)" ).lower()

		if confirm == "y" or confirm == "yes":
			bulkMovePlates(bulkScanBarcodes(), shelf, operator)
			complete = True
		elif confirm == "exit":
			return

	#store multiple plates into a shelf on the fridge and checks against database and rellocates to new shelf
	return 

def disposePlates():
	return 

def seqPlatesScanner():
	return

def seqPlateLookup():
	return

def plateLookup():
	return

def interpreter(command):
	if command == "help":
		print("List of Commands:" +
			"\n checkin: check plates into shelf" + 
			"\n search: search for set of plates" + 
			"\n export: exports database to CSV" + 
			"\n backup: saves backup of database")
	elif command == "checkin" or command =="c":
		checkIn()
	elif command == "print" or command =="p":
		printDBBarcodes()
	elif command == "export" or command =="e":
		printAllDB()
	elif command == "search" or command =="s":
		search()
	elif command == "backup" or command =="b":
		backupDatabase()
		print("Backup Successful")
	else: 
		return


# Testing Code
# Features: Search Plate, Move Plate, Register Plate, 

# labDB.append(item("B001", "FG001_R1", "Kenny Ma"))
# labDB.append(item("B002", "FG001_R1", "Kenny Ma"))
# labDB.append(item("B003", "FG001_R1", "Kenny Ma"))
# labDB.append(item("B004", "FG001_R1", "Kenny Ma"))
# labDB.append(item("B005", "FG001_R1", "Kenny Ma"))
# labDB.append(item("B006", "FG001_R2", "Kenny Ma"))
# # printDBBarcodes()

#Main Loop intro
labDB = loadDatabase()
print("Loaded Fridge Database with " + str(len(labDB)) + " Items")


while main:
	command = input("Enter Command:").lower()
	interpreter(command)

#Graphical User Interface
