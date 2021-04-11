import os
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE1_URL','sqlite:///students.sqlite3') # Dataase URI, get in HEROKU

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name
        
@app.route('/')
def show_all():
    return render_template('show_all.html', students = students.query.all())

@app.route('/form', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        student = students(request.form['name'])

        db.session.add(student)
        db.session.commit() 
        return redirect(url_for('show_all'))

    return render_template('new.html')


if __name__ == '__main__':
    app.run(port=5000)