# Importing the modules
# Render_template renders HTML, request handles form data
# Redirect and url_for direct users to a route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Todo Model class
# Define the columns (attributes) for the class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add the repr method
    # This is a special Python method that returns
    # a string representing the object
    def __repr__(self):
        return f'<Todo id={self.id} title={self.title} done={self.done} created_at={self.created_at}>'

# Create the database and table to hold the "To Do"s
with app.app_context():
    db.create_all()

# Create a home route that displays the To Do list
@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

# Create a route for adding a new To Do to the database
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

# Create a route to mark a To Do item as done
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete a To Do item
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger & shows the stack trace if an error occurs
# Debug mode also reloads the page if you change the
# code so you don't need to restart the server.
if __name__ == '__main__':
    app.run(debug=True)