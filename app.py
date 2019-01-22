# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
import config
from models import Post, Comment
from exts import db
from decorators import log_required
from collections import OrderedDict
from datetime import datetime
from math import ceil


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# @app.route('/')
# def index():
#     context = {
#         'questions': Question.query.order_by('-create_time').all()
#     }
#     return render_template('index.html', **context)


'''index page showing all posts paginated'''
@app.route('/')
def show_entries():
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False)
    entries=pagination.items
    entries_all = Post.query.all()

    tagss = []
    for i in entries_all:
        tagss.append(i.tag.capitalize())
    tags = set(tagss)

    tag_num = []
    for i in tags:
        count_tag = tagss.count(i)
        tag_num.append(count_tag)

    d = dict(zip(tags, tag_num))
    dict_tag = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

    return render_template('show_entries.html', entries=entries, pagination=pagination,
        tags=tags, tag_num=tag_num, dict_tag=dict_tag)


@app.route('/lists')
def entries_lists():
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page,per_page=app.config['PER_PAGE'],error_out=False)
    entries=pagination.items
    entries_all = Post.query.all()

    tagss = []
    for i in entries_all:
        tagss.append(i.tag.capitalize())
    tags = set(tagss)

    tag_num = []
    for i in tags:
        count_tag = tagss.count(i)
        tag_num.append(count_tag)

    d = dict(zip(tags, tag_num))
    dict_tag = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

    return render_template('entries_lists.html', entries=entries, pagination=pagination,
        tags=tags, tag_num=tag_num, dict_tag=dict_tag)



@app.route('/tags-lists/<tag>')
def show_tags_lists(tag):
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(tag=tag).order_by(Post.id.desc()).paginate(page,per_page=app.config['PER_PAGE'],error_out=False)
    entries=pagination.items

    entries_all = Post.query.all()

    tagss = []
    for i in entries_all:
        tagss.append(i.tag.capitalize())
    tags = set(tagss)

    tag_num = []
    for i in tags:
        count_tag = tagss.count(i)
        tag_num.append(count_tag)

    d = dict(zip(tags, tag_num))
    dict_tag = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

    return render_template('entries_lists.html', entries=entries, pagination=pagination, dict_tag=dict_tag)



@app.route('/tags/<tag>')
def show_tags(tag):
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(tag=tag).order_by(Post.id.desc()).paginate(page,per_page=app.config['PER_PAGE'],error_out=False)
    entries=pagination.items

    entries_all = Post.query.all()

    tagss = []
    for i in entries_all:
        tagss.append(i.tag.capitalize())
    tags = set(tagss)

    tag_num = []
    for i in tags:
        count_tag = tagss.count(i)
        tag_num.append(count_tag)

    d = dict(zip(tags, tag_num))
    dict_tag = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

    return render_template('show_entries.html', entries=entries, pagination=pagination, dict_tag=dict_tag)





'''url for each post and its guest comments'''
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    # comments = post.comments.all()
    comments = post.comments.order_by(Comment.id.desc())
    if request.method == 'POST':
        addcomments = Comment(reply=request.form['reply'], post=post, replytime=datetime.now())
        db.session.add(addcomments)
        # return redirect(url_for('show_entries'))

    entries_all = Post.query.all()

    tagss = []
    for i in entries_all:
        tagss.append(i.tag.capitalize())
    tags = set(tagss)

    tag_num = []
    for i in tags:
        count_tag = tagss.count(i)
        tag_num.append(count_tag)

    d = dict(zip(tags, tag_num))
    dict_tag = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

    return render_template('post.html', post=post, comments=comments, dict_tag=dict_tag)

'''add a post if the admin is logged in'''
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        post=Post(title=request.form['title'], tag=request.form['tag'].capitalize(), text=request.form['text'], timestamp=datetime.now())
        db.session.add(post)
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    return render_template('add.html')

'''delete a post if admin is logged in'''
@app.route('/delete/<int:id>')
def delete_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        flash('The post has been deleted')
        return redirect(url_for('show_entries'))

@app.route('/update_entry/<int:id>')
def update_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    post = Post.query.get_or_404(id)
    id = post.id
    title = post.title
    text = post.text
    tag = post.tag
    return render_template('update.html', id=id, title=title, text=text, tag=tag)

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        post = Post.query.get_or_404(id)
        post.title = request.form['title']
        post.text = request.form['text']
        post.tag = request.form['tag'].capitalize()
        post.timestamp = datetime.now()
        db.session.add(post)
        db.session.commit()

        flash('The post has been updated')
        return redirect(url_for('show_entries'))
    else:
        return render_template('update.html')





'''login page with error message'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

'''log admin out; return None if key 'logged_in' doesn't exsit'''
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()





# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         telephone = request.form.get('telephone')
#         password = request.form.get('password')
#         # print(telephone)
#         # print(password)
#         user = User.query.filter(User.telephone == telephone, User.password == password).first()
#         # print(user)
#         # return telephone
#
#         if user:
#             # print("hello")
#             session['user_id'] = user.id
#             session.permanent = True
#             flash('You have logged in!')
#             return redirect(url_for('index'))
#         else:
#             return "手机号码或者密码输入错误"
#
#
# @app.route('/logout')
# def logout():
#     # session.clear()
#     session.pop('user_id', None)
#     flash('You have logged out!')
#     return redirect(url_for('index'))
#
# # @app.route('/logout/')
# # def logout():
# #     session.clear()
# #     return redirect(url_for('login'))
#
#
# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     else:
#         telephone = request.form.get('telephone')
#         username = request.form.get('username')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#
#         user = User.query.filter(User.telephone == telephone).first()
#         if user:
#             return "该手机号码已经注册，请更换手机号码"
#         else:
#             if password1 != password2:
#                 return "两次输入密码不一致，请检查"
#             else:
#                 user = User(telephone=telephone, username=username, password=password1)
#                 db.session.add(user)
#                 db.session.commit()
#                 flash("You've registered! Please login in")
#                 return redirect(url_for('login'))
#
#
# @app.route('/question/', methods=['GET', 'POST'])
# @log_required
# def question():
#     if request.method == 'GET':
#         return render_template('question.html')
#     else:
#         title = request.form.get('title')
#         content = request.form.get('content')
#         question = Question(title=title, content=content)
#         user_id = session.get('user_id')
#         user = User.query.filter(User.id == user_id).first()
#         question.author = user
#         db.session.add(question)
#         db.session.commit()
#         return redirect(url_for('index'))
#
#
# @app.route('/detail/<question_id>')
# def detail(question_id):
#     question_model = Question.query.filter(Question.id == question_id).first()
#     return render_template('detail.html', question=question_model)
#
#
# @app.route('/add_comment/', methods=['POST'])
# @log_required
# def add_comment():
#     content = request.form.get('content')
#     question_id = request.form.get('question_id')
#
#     comment = Comment(content=content)
#     user_id = session['user_id']
#     user = User.query.filter(User.id == user_id).first()
#     comment.author = user
#     question = Question.query.filter(Question.id == question_id).first()
#     comment.question = question
#     db.session.add(comment)
#     db.session.commit()
#     return redirect(url_for('detail', question_id=question_id))
#
#
# if __name__ == '__main__':
#     app.debug = True
#     app.run()
