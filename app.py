#Flask stuff - Clive
from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key=urandom(32)

#helper method
#return true if a user is logged in
def checkSession():
    return "user" in session

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
    return return_template("Register.html")
    
@app.route("/Authorize", methods=["GET", "POST"])
def Authorize():
    #if user is already logged in, redirect to Welcome
    if checkSession():
        return redirect(url_for("Welcome"))
    #check if the submitted login information is correct, and then store a session
    if authorize(request.form["username"], request.form["password"]):
        session["username"] = request.form["username"]
    #if the submitted login information is not correct, redirect to Welcome, flash a message
    else:
        "FLASH MESSAGE HERE"
        return redirect(url_for("Login"))
    


@app.route("/Welcome", methods=["GET", "POST"])
def Welcome():
        user = session["username"]
        #renders Welcome template, and passes variables for username, and an array of edited, and not-edited stories
        return render_template("Welcome.html", username = user, \
        titles_edited= database.checkEdited(getUserId(user)), \
        titles_not_edited = database.check(getUserId(user)))


    
    
if __name__ == '__main__':
    app.debug = True
    app.run()
