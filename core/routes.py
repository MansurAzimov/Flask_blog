from flask import render_template,redirect,url_for,flash,request
from core import app

@app.route ('/')
def index():
    return render_template ('index.html')

@app.route ('/post')
def post():
    return render_template ('post.html')

@app.route ('/post_delete')
def post_delete():
    #Удаление поста из базы данных
    flash('Пост удален','danger')
    return redirect(url_for('index'))

@app.route ('/new_post', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get ('title')
        content = request.form.get ('content')
        with open ('post.txt', 'a', encoding = 'utf-8') as f:
            f.write (title + '\n')
            f.write (content + '\n')
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


