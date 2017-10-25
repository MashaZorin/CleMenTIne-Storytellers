#Database stuff - Tiffany

import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

f="../data/dummy.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops



# FUNCTIONS!!!

def checkUsernames(username):
    #checks if username is taken
    #called when user registers onto our site
    #returns True if username is taken, returns False if username is not taken
    cm = "SELECT user FROM userInfo;"
    for i in c.execute(cm):
        if username == i[0].encode("ascii"):
            return True
    return False

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

def addLine(line, story_title, userid):
    #adds a line into a story
    #called when a user submits an edit to a story
    story_id = getStoryID(story_title)
    cm = 'UPDATE edited SET '

# END FUNCTIONS



# START ALL OUR GET FUNCTIONS

def getUserID(username):
    cm = 'SELECT id FROM userInfo WHERE user = "%s";' %username
    for i in c.execute(cm):
        x = i[0]
    return x

def getStoryID(title):
    cm = 'SELECT story_id FROM log WHERE title = "%s";' %title
    for i in c.execute(cm):
        x = i[0]
    return x

def getStory(title):
    cm = 'SELECT body FROM log WHERE title = "%s";' %title
    for i in c.execute(cm):
        x = i[0].encode("ascii")
    return x

# END ALL OUR GET FUNCTIONS



# START ALL OUR TESTS

# updateUsers('"debra"', '"itsstorytime"') -> function works
print authorize('alice', 'pass') # should print true
print authorize('alice', 'pas') # should print false
print checkUsernames('alice') # should print true
print checkUsernames('eliza') # should print false
print getUserID('alice')
print getUserID('bob')
print getUserID('charlie')
print getUserID('debra')

# END ALL OUR TESTS



db.commit() #save changes
db.close()  #close database