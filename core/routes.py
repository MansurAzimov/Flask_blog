from flask import render_template,redirect,url_for,flash,request
from core import app,db

@app.route ('/')
def index():
    posts = db.execute('SELECT * FROM posts ORDER BY id DESC;').fetchall()
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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'admin@mail.ru' and password == 'admin':
            #Login
            return redirect (url_for('index'))
        else:
            flash('Данные для входа не верные','danger')
    return render_template ('login.html')

@app.route ('/registration', methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        with open ('post.txt', 'a', encoding = 'utf-8') as f:
            f.write (email + '\n')
            f.write (password + '\n')
        flash('Профиль создан','success')
        return redirect(url_for('index'))
    return render_template ('registration.html')

@app.route ('/logout')
def logout():
    #Logout
    return redirect(url_for('index'))

@app.route ('/add_comment', methods=['POST'])
def add_comment():
        message = request.form.get('message')
        with open ('post.txt', 'a', encoding = 'utf-8') as f:
            f.write (message + '\n')
        flash('Спасибо','success')
        return redirect(url_for('post'))


