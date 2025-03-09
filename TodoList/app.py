"""
 Flask URL: https://flask.palletsprojects.com/en/stable/quickstart/
 BootStrap: https://getbootstrap.com/docs/5.3/getting-started/introduction/
 SQLite Viewer: https://inloop.github.io/sqlite-viewer/
"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

# Store CST TZ using Python library "pytz"
cst_timezone = pytz.timezone('America/Chicago')

# Setup SQLite DB using python library "SQLAlchemy"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setup thedefinition of Columns for DB using Python Class
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(cst_timezone))

    def __repr__(self) -> str:                  # A special method (__repr__) that defines how an instance of Todo will be represented as a string.
        return f"{self.sno} - {self.title}"     # Will return a string in the format "sno - title".

# Deletes all the data of table before running the app
# Keep this whenever need to clear the data of table, later can be removed
@app.before_request
def create_tables():
    db.create_all()

# GET → Fetch and display data.
# POST → Submit form data (e.g., adding a new to-do item).
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':              # Checks if the request method is POST (meaning a form was submitted).
        title = request.form['title']       # Retrieving Form Data
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc) # Creates a new Todo object with the extracted title and description.
        db.session.add(todo)                # Adds the new Todo object to the database session (staging area).
        db.session.commit()                 # Commits (saves) the changes to the database
    allTodo = Todo.query.all()              # Queries the database to retrieve all Todo items. Stores them in allTodo (a list of Todo objects).
    return render_template('index.html', allTodo=allTodo)
# render_template() is a Flask function that loads an HTML file from the templates folder and injects dynamic data into it.
# It allows us to send variables from Python (backend) to the HTML page (frontend) for rendering.
# allTodo=allTodo:
# The left side (allTodo) is the variable name that will be used in the HTML template.
# The right side (allTodo) is the actual list of to-do items retrieved from the database.
# This means index.html will have access to all the to-do items stored in the database.
# Flask searches for index.html inside the templates/ folder.
# It injects the allTodo data into the template.
# The template uses Jinja2 syntax ({{ ... }} or {% ... %}) to display dynamic data.

# Creates sepearate page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Main function of python
if __name__ == "__main__":
    app.run(debug=True, port=8000)