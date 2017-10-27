#Database stuff - Tiffany

import sqlite3   #enable control of an sqlite database

def openDatabase():
    f="data/dummy.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    return db, db.cursor()    #facilitate db ops

def closeDatabase(db):
    db.commit() #save changes
    db.close()  #close database

# FUNCTIONS!!!

def checkUsernames(username):
    #checks if username is taken
    #called when user registers onto our site
    #returns True if username is taken, returns False if username is not taken
    db, c = openDatabase()
    cm = "SELECT user FROM userInfo;"
    for i in c.execute(cm):
        if username == i[0].encode("ascii"):
            closeDatabase(db)
            return True
    closeDatabase(db)
    return False

def checkTitles(title):
    #checks if username is taken
    #called when user registers onto our site
    #returns True if username is taken, returns False if username is not taken
    db, c = openDatabase()
    cm = "SELECT title FROM log;"
    for i in c.execute(cm):
        if title == i[0].encode("ascii"):
            closeDatabase(db)
            return True
    closeDatabase(db)
    return False

def updateUsers(username, password): 
    #adds a new record in the userInfo table with the username, password, and a userID (found in function)
    #called when user registers onto our site
    db, c = openDatabase()
    cm = "SELECT COUNT(*) FROM userInfo;"
    for i in c.execute(cm):
        userID = i[0]
    cm = 'INSERT INTO userInfo VALUES("%s", "%s", %d)' %(username, password, userID)
    c.execute(cm)
    closeDatabase(db)

def authorize(username, password):
    #checks whether a person's password matches their username
    #called by authorize() in app.py
    db, c = openDatabase()
    cm = 'SELECT password FROM userInfo WHERE user = "%s";' %username
    x = c.execute(cm)
    for i in x:
        true_pass = i
    closeDatabase(db)
    return password == true_pass[0].encode("ascii")

def addLine(line, story_title, userid):
    #adds a line into a story
    #called when a user submits an edit to a story
    db, c = openDatabase()
    storyid = getStoryID(story_title)
    cm = 'INSERT INTO edited VALUES (%d, %d)' %(userid, storyid)
    c.execute(cm)
    cm = 'UPDATE log SET lastLine = "%s" WHERE storyId = %d' %(line, storyid)
    c.execute(cm)
    x = c.execute('SELECT body FROM log WHERE storyId = %d')[0] %storyid

# END FUNCTIONS



# START ALL OUR GET FUNCTIONS

def getUserID(username):
    db, c = openDatabase()
    cm = 'SELECT id FROM userInfo WHERE user = "%s";' %username
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getStoryID(title):
    db, c = openDatabase()
    cm = 'SELECT storyId FROM log WHERE title = "%s";' %title
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getStory(title):
    db, c = openDatabase()
    cm = 'SELECT body FROM log WHERE title = "%s";' %title
    for i in c.execute(cm):
        x = i[0].encode("ascii")
    closeDatabase(db)
    return x

def checkEdited():
    return "edited"

# END ALL OUR GET FUNCTIONS



# START ALL OUR TESTS

# updateUsers('"debra"', '"itsstorytime"') -> function works
'''print authorize('alice', 'pass', c) # should print true
print authorize('alice', 'pas', c) # should print false
print checkUsernames('alice', c) # should print true
print checkUsernames('eliza', c) # should print false
print checkTitles('DW', c) # should print true
print checkTitles('wrong', c) # should print false
print getUserID('alice', c)
print getUserID('bob', c)
print getUserID('charlie', c)
print getUserID('debra', c)
print getStoryID("Tail", c)
print getStoryID("DW", c)
print getStory("Tail", c)
print getStory("DW", c)'''

# END ALL OUR TESTS