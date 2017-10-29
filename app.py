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
    database.updateUsers(postedUsername, postedPassword)
    flash ("Account succesfully created. Please login again")
    return redirect(url_for("Root"))
            
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
    tempUserID = session["userID"]
    #renders Welcome template, and passes variables for username, and an array of edited, and not-edited stories
    #print database.getEdited(tempUserID)
    #print database.getNotEdited(tempUserID)
    return render_template("Welcome.html", username = tempUserID, \
    titles_edited = database.getEdited(tempUserID), \
    titles_not_edited = database.getNotEdited(tempUserID))

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
    tempUserID = session["userID"]
    #if user has already edited this story, redirect to Welcome
    title = request.args["title"]
    #works with issue of user trying to edit a story they have already edited (commented out)
    if title not in database.getNotEdited(tempUserID):
        print title
        print database.getNotEdited(tempUserID)
        flash("You have already edited this story")
        return redirect(url_for("Welcome"))
    #if user has not yet edited this story, render EditStory.html template
    return render_template("EditStory.html", title=title)
    #ADD THIS INTO RENDER_TEMPLATE LINE --> lastLine = database.getLastLine(request.args["title"])

@app.route("/EditStoryAction", methods=["GET", "POST"])
def EditStoryAction():
    database.addLine(request.form["line"], request.form["title"], session["userID"])
    return redirect(url_for("ViewStory", title=request.form["title"]))
    
@app.route("/ViewStory")
def ViewStory():
    #render viewStory template, passing args for title (from query string), and story 
    render_template("viewStory.html", title=request.args["title"], story = database.getStory(request.args["title"]))
    
    
    




    
    
if __name__ == '__main__':
    app.debug = True
    app.run()
