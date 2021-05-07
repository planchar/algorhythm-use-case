#Import the flask module
from flask import Flask, redirect, url_for, render_template, request

#Create a Flask constructor. It takes name of the current module as the argument
# DEBUG = True
app = Flask(__name__)

#Create a route decorator to tell the application, which URL should be called for the #described function and define the function

@app.route('/', methods=["GET", "POST"])
def index():
    # if POST, send url to render summary
    if request.method == "POST":
        url = request.form["url"]
        return redirect(url_for("summarize", url=url))
    # if GET, show form
    else:
        return render_template("index.html")

@app.route('/summarize')
def summarize(url):
    # take the url, pass it to a summarizer
    # return the result in a webpage
    # return render_template("summary.html")
    return render_template("summarize.html")

@app.route('/')
def site(url):
    # return render_template("summary.html")
    return f"<h1>{url}<h1>"

#Create the main driver function
if __name__ == '__main__':
    #call the run method
    app.run(debug=True)