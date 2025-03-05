# Importing the modules
# Render_template renders HTML, 
# request handles form data
# Redirect and url_for direct users to a route in the website navigation

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app (__name__ will call the name method)
app = Flask(__name__)

# Configure SQLite database

#add the URI = uniform resource identifier, the path to the database, name of the database (todos.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

# Disable the SQLALCHEMY_TRACK_MODIFICATIONS: (set to False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#new variable db, create a new instance of the SQLAlchemy class (will connect to database, get columns, etc.)
db = SQLAlchemy(app)

# Define Todo Model class (models a todo list item that is stored in the database)
# Define the columns (attributes) for the class
class Todo(db.Model):
    #This is the orm that SQLAlchemy uses to create the table in the database: 
    id = db.Column(db.Integer, primary_key=True)

    #(100 is the max number of characters:)
    #nullable=False means that the title is required:
    title = db.Column(db.String(100), nullable=False)

    #either complete or incomplete:
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add the repr method
    # This is a special Python method that returns
    # a string representing the object (so it's easy for other developers read what you were going after:)
    def __repr__(self):
        return f'<Todo id={self.id} title={self.title} done={self.done} created_at={self.created_at}>'

# Create the database and table to hold the "To Do"s
with app.app_context():
    db.create_all()

# Create a home route that displays the To Do list
#forward slash indicates the default route
@app.route('/')
#if the user goes to the home route, the index function will be called 
def index():
    #will query the database for all the To Do items:
    #order_by will order the items by the created_at column in descending order:
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    #this is what will be displayed in the user's browswer:, this is a Jinga function: 
    return render_template('index.html', todos=todos)

# Create a route for adding a new To Do to the database
@app.route('/add', methods=['POST'])
def add():
    # Get the title from the form:
    title = request.form.get('title')
    if title: #if title is not null, create a new title
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
        #else, return the user to the home route:
    return redirect(url_for('index'))

# Create a route to mark a To Do item as done
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    #update the database to mark the item as done:
    # if something goes wrong, return a 404 error:
    todo = Todo.query.get_or_404(todo_id)
    #mark the item as done:
    todo.done = not todo.done
    #commit the changes to the database:
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete a To Do item
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    #check if a database record exists with the given id number:
    #if there is no matching record, return a 404 error:
    todo = Todo.query.get_or_404(todo_id)
    #now we know it exists, delete the record: (todo is passed in as an argument)
    db.session.delete(todo)
    #make sure change is saved:
    db.session.commit()
    #return the user to the home route:
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger & shows the stack trace if an error occurs
# Debug mode also reloads the page if you change the
# code so you don't need to restart the server.
if __name__ == '__main__':
    app.run(debug=True) 