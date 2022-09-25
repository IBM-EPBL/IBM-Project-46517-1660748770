from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
  return render_template("Home.html")

@app.route("/about")
def about():
  return render_template("About.html")

@app.route("/signin")
def signin():
  return render_template("SignIn.html")

@app.route("/signup")
def signup():
  return render_template("SignUp.html")

@app.route("/forgot")
def forgot():
  return render_template("forgot.html")