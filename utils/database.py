#Database stuff - Tiffany

import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

f="../data/dummy.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

def updateUsers(username, password): 
    #adds a new record in the userInfo table with the username, password, and a userID (found in function)
    #called when user registers onto our site
    cm = "SELECT COUNT(*) FROM userInfo;"
    for i in c.execute(cm):
        userID = i[0]
    cm = 'INSERT INTO userInfo VALUES("%s", "%s", %d)' %(username, password, userID)
    c.execute(cm)

def authorize(username, password):
    #checks whether a person's password matches their username
    #called by authorize() in app.py
    cm = 'SELECT password FROM userInfo WHERE user = "%s";' %username
    x = c.execute(cm)
    for i in x:
        true_pass = i
    return password == true_pass[0].encode("ascii")

# updateUsers('"debra"', '"itsstorytime"') -> function works
print authorize('alice', 'pass') # should print true
print authorize('alice', 'pas') # should print false

db.commit() #save changes
db.close()  #close database