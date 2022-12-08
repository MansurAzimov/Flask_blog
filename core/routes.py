from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,current_user

from core import app,db
from core.models import User



@app.route ('/')
def index():
    posts = []
    return render_template ('index.html',posts=posts)

@app.route ('/post/ <int:id>')
def post():
    post = db.execute('SELECT * FROM posts WHERE id = :id', {'id': id}).fetchone()
    return render_template ('post.html', post=post)

@app.route ('/post_delete/<int:id>')
def post_delete(id):
    db.execute('DELETE FROM posts WHERE id = :id',{'id': id})
    db.commit
    flash('Пост удален','danger')
    return redirect(url_for('index'))

@app.route ('/new_post', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get ('title')
        body = request.form.get ('body')
        db.execute('INSERT INTO posts(title,body) VALUES (:title, :body)',{'title': title, 'body': body })
        db.commit()
        flash('Пост создан','success')
        return redirect(url_for('index'))
    return render_template ('new_post.html')

@app.route ('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect (url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect (url_for('index'))
        else:
            flash('Данные для входа не верные','danger')
    return render_template ('login.html')

@app.route ('/registration', methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash ('Профиль с таким именем существует', 'danger')
            return redirect(url_for('registration'))
        user = User( username = username, password=password )
        db.session.add (user)
        db.session.commit ()
        flash('Профиль создан','success')
        return redirect(url_for('login'))
    return render_template ('registration.html')

@app.route ('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route ('/add_comment', methods=['POST'])
def add_comment():
        message = request.form.get('message')
        with open ('post.txt', 'a', encoding = 'utf-8') as f:
            f.write (message + '\n')
        flash('Спасибо','success')
        return redirect(url_for('post'))


