from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,current_user,login_required

from core import app,db
from core.models import User,Post,Comment



@app.route ('/')
def index():
    posts = Post.query.all()
    return render_template ('index.html',posts=posts)

@app.route ('/post/<int:id>')
def post(id):
    post = Post.query.get(id)
    return render_template ('post.html', post=post)


@app.route ('/new_post', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get ('title')
        body = request.form.get ('body')
        post = Post(title=title, body=body, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
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

@app.route ('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
        message = request.form.get('message')
        comment = Comment(message=message, author_id=current_user.id,post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Спасибо','success')
        return redirect(url_for('post',id=post_id))

@app.route('/post_delete/<int:post_id>', methods=['GET'])
@login_required
def post_delete(post_id):
    try:
        p = Post.query.filter(Post.id == post_id).delete()
        db.session.commit()
        flash('Пост удален','success')
    except:
        db.session.rollback()
    return redirect(url_for('index'))

