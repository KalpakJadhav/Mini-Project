from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


from sqlalchemy import desc
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'Todo {self.sno} - {self.title}'

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        due_time_str = request.form['due']
        due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')
        todo = Todo(title=title, description=desc, due_time=due_time)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        due_time_str = request.form['due']
        due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = desc
        todo.due_time = due_time
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = Todo.query.filter(Todo.title.contains(query) | Todo.description.contains(query)).all()
    return render_template('index.html', allTodo=results)
if __name__ == '__main__':
    app.run(debug=True,port=8000)
