#Database stuff - Tiffany

import sqlite3   #enable control of an sqlite database

f="../data/dummy.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

# FUNCTIONS!!!

def checkUsernames(username, c):
    #checks if username is taken
    #called when user registers onto our site
    #returns True if username is taken, returns False if username is not taken
    cm = "SELECT user FROM userInfo;"
    for i in c.execute(cm):
        if username == i[0].encode("ascii"):
            return True
    return False

def checkTitles(title, c):
    #checks if username is taken
    #called when user registers onto our site
    #returns True if username is taken, returns False if username is not taken
    cm = "SELECT title FROM log;"
    for i in c.execute(cm):
        if title == i[0].encode("ascii"):
            return True
    return False

def updateUsers(username, password, c): 
    #adds a new record in the userInfo table with the username, password, and a userID (found in function)
    #called when user registers onto our site
    cm = "SELECT COUNT(*) FROM userInfo;"
    for i in c.execute(cm):
        userID = i[0]
    cm = 'INSERT INTO userInfo VALUES("%s", "%s", %d)' %(username, password, userID)
    c.execute(cm)

def authorize(username, password, c):
    #checks whether a person's password matches their username
    #called by authorize() in app.py
    cm = 'SELECT password FROM userInfo WHERE user = "%s";' %username
    x = c.execute(cm)
    for i in x:
        true_pass = i
    return password == true_pass[0].encode("ascii")

def addLine(line, story_title, userid, c):
    #adds a line into a story
    #called when a user submits an edit to a story
    storyid = getStoryID(story_title)
    cm = 'INSERT INTO edited VALUES (%d, %d)' %(userid, storyid)
    c.execute(cm)
    cm = 'UPDATE '

# END FUNCTIONS



# START ALL OUR GET FUNCTIONS

def getUserID(username, c):
    cm = 'SELECT id FROM userInfo WHERE user = "%s";' %username
    for i in c.execute(cm):
        x = i[0]
    return x

def getStoryID(title, c):
    cm = 'SELECT storyId FROM log WHERE title = "%s";' %title
    for i in c.execute(cm):
        x = i[0]
    return x

def getStory(title, c):
    cm = 'SELECT body FROM log WHERE title = "%s";' %title
    for i in c.execute(cm):
        x = i[0].encode("ascii")
    return x

# END ALL OUR GET FUNCTIONS



# START ALL OUR TESTS

# updateUsers('"debra"', '"itsstorytime"') -> function works
print authorize('alice', 'pass', c) # should print true
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
print getStory("DW", c)

# END ALL OUR TESTS



db.commit() #save changes
db.close()  #close database