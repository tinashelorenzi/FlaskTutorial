from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",name="Tinashe")

@app.route("/search")
def search_page():
    query = request.args.get('word')
    return "Hello "+query

@app.route("/hi")
def hi():
    return "Hellon we are here"

@app.route("/moks")
def greet_moks():
    return "Hello, my name is Moks!"

@app.route("/contact")
def contact_page():
    return render_template("contact.html",title="Contact Us")

@app.route("/submit",methods=['POST'])
def handleSubmitContact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    with open('forms.txt','a') as f:
        f.write(f"{name} | {email} | {subject} | {message} \n")
    f.close()
    return render_template("success.html",name=name)