# Morning
# Midday
# Night

import sqlite3
conn = sqlite3.connect("storage.db")

c = conn.cursor()

def createTables():
	# Create table
	c.execute("CREATE TABLE if not exists users (firstName text, secondName text, amazonID text, userID INTEGER PRIMARY KEY AUTOINCREMENT)")
	c.execute("CREATE TABLE if not exists drugAllocations (userID INTEGER, slotNumber INTEGER, inUse INTEGER, drugName TEXT, drugQuantity INTEGER, dose INTEGER, morning INTEGER, lunch INTEGER, evening INTEGER )")
	c.execute("CREATE TABLE if not exists drugHistory (userID INTEGER, date TEXT, drugName TEXT, dose INTEGER)")
	conn.commit()

createTables()

# Insert a row of data
# c.execute("INSERT INTO users (firstName, secondName, amazonID) VALUES ('Jane', 'Jones', 'abc987')")
c.execute("INSERT INTO drugAllocations VALUES ("+ userID + ", 0, 1, 'Paracetamol', 14, 2, 1, 0, 0)")

#if c.execute("SELECT * FROM users WHERE userID=3").fetchone():
#	print("UserID found!")

# Save (commit) the changes


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()