#Flask stuff - Clive
from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils import database

app = Flask(__name__)
app.secret_key=urandom(32)

#helper method
#return true if a user is logged in
def checkSession():
    return "userID" in session

@app.route("/")
def Root():
    #if user is already logged in, redirect to Welcome
    if checkSession():
        return redirect(url_for("Welcome"))
    #otherwise return the template for Login
    return render_template("Login.html")
    
@app.route("/Register")
def Register():
    #if user is already logged in, redirect to Welcome
    if checkSession():
        return redirect(url_for("Welcome"))
    #otherwise return the template for Register
    return render_template("Register.html")
    
@app.route("/CreateAccount", methods=["GET", "POST"])
def CreateAccount():
    #if user is already logged in, redirect to Welcome
    if checkSession():
        return redirect(url_for("Welcome"))
    #if username exits, flash message and redirect to Register
    postedUsername = request.form["username"]
    postedPassword = request.form["password"]
    if database.checkUsernames(postedUsername):
        flash("Username already taken")
        return redirect(url_for("Register"))
    #othwerwise, create the account and redirect to Root
    database.createAccount(postedUsername, postedPassword)
    flash ("Account succesfully created. Please login again")
    return ridirect(url_for("Root"))
            
@app.route("/Authorize", methods=["GET", "POST"])
def Authorize():
    #if user is already logged in, redirect to Welcome
    if checkSession():
        return redirect(url_for("Welcome"))
    #check if the submitted login information is correct, and then store a session with the userId
    postedUsername = request.form["username"]
    postedPassword = request.form["password"]
    if database.checkUsernames(postedUsername):
        if database.authorize(postedUsername, postedPassword):
            session["userID"] = database.getUserID(postedUsername)
            return redirect(url_for("Welcome"))
    #if the submitted login information is not correct, redirect to Welcome, flash a message
    flash("Incorrect username, password combination")
    return redirect(url_for("Root"))

@app.route("/Welcome", methods=["GET", "POST"])
def Welcome():
    #session.pop("userID")
    #if user is not logged in, redirect to Root
    if not checkSession():
        return redirect(url_for("Root"))
    #otherwise, acess inputted data from form
    tempUserId = session["userID"]
    #renders Welcome template, and passes variables for username, and an array of edited, and not-edited stories
    return "Welcome place holder"
    
    #add this stuff when database methods are ready
    '''render_template("Welcome.html", userId = tempUserId, \
    titles_edited = database.checkEdited(tempUserId), \
    titles_not_edited = database.checkNotEdited(tempUserId))'''

@app.route("/Logout", methods=["GET", "POST"])
def Logout():
    #if user is logged in, remove the session
    if checkSession():
        session.pop("userID")
        flash("Successfuly logged out")
    #redirect to Root regardless
    return redirect(url_for("Root"))


@app.route("/EditStory")
def EditStory():
    #if user is not logged in, redirect to root
    if not checkSession():
        return redirect(url_for("Root"))
    tempUserId = session["userId"]
    #if user has already edited this story, redirect to Welcome
    title = request.method("title")
    if title not in database.checkEdited(tempUserId):
        Flash("You have already edited this story")
        return redirect(url_for("Welcome"))
    #if user has not yet edited this story, render EditStory.html template
    return render_template("EditStory.html")
    
    




    
    
if __name__ == '__main__':
    app.debug = True
    app.run()
