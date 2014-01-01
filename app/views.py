# Import the app itself
from app import app, db, lm, path, main_path
import os
import datetime

from werkzeug import secure_filename
from wtforms import fields

# Import the functions and classes from flask and it's extensions
from flask import abort, render_template, redirect, request, url_for, flash, g, session, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

# Import the forms
from forms import LogInForm, EditPost, EditInfo

# Import the models from the database
from models import User, Post, Info

from sqlalchemy import func, desc

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

# This is in accordance with usage of current_user from Flask-Login

@lm.user_loader
def load_user(id):
	return User.query.get(id)


@app.before_request
def before_request():
	g.user = current_user
	g.info = Info.query.first()
	app.config['UPLOAD_FOLDER'] = url_for('static', filename='images')




###########################################################
#														  #	
#					  USER VIEWS						  #
#														  #	
###########################################################
	
@app.route('/')
def index():
	posts = Post.query.order_by(desc(Post.publish_date)).filter(Post.publish_date != None).all()

	for item in posts:
		item.publish_date =  item.publish_date.strftime("%B %d, %Y")
	return render_template('index.html', page_title = 'Posterious', posts = posts)



@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return render_template('login.html', page_title = 'Sign In', message="You are already logged in!")

	form = LogInForm() 

	if form.validate_on_submit():
		user = form.get_user()
		login_user(user)
		flash("Logged In Successfully")
		return redirect(request.args.get('next') or url_for('admin'))

	return render_template('login.html', page_title = 'Sign In', form = form)

@app.route('/logout')
def logout():
	logout_user()
	flash("Logged Out  Successfully")
	return redirect(url_for('index'))


@app.route('/<post_slug>')
def post(post_slug):
	post = Post.query.filter(func.lower(Post.title) == func.lower(post_slug)).first()
	
	if post == None:
		return "404"

	if post.publish_date:
		post.publish_date = post.publish_date.strftime("%B %d, %Y")
	else:
		return "404"
	if post.tags:
		tags = post.tags.split(',')
	else:
		tags = None
	return render_template('post.html', page_title = post.title, post = post, tags = tags)



###########################################################
#														  #	
#					  ADMIN VIEWS						  #
#														  #	
###########################################################

@app.route('/admin')
@login_required
def admin():
	posts = Post.query.order_by(desc(Post.publish_date)).all()
	for item in posts:
		if item.publish_date:
			item.publish_date =  item.publish_date.strftime("%B %d, %Y")
	return render_template('admin.html', page_title = 'Admin', posts = posts)


@app.route('/admin/create', methods = ['GET', 'POST'])
@login_required
def create_new_post():
	form = EditPost()

	if request.method == 'POST':
		if request.form['submit'] == 'Publish' and form.validate_on_submit():
			x = Post(title = form.title.data, content = form.content.data, tags = form.tags.data, publish_date = datetime.datetime.now())
			db.session.add(x)
			db.session.commit()
			if x:
				flash("Post Published Successfully")
			return redirect(url_for('admin'))
		elif request.form['submit'] == 'Save Draft' and form.validate_on_submit():
			x = Post(title = form.title.data, content = form.content.data, tags = form.tags.data,)
			db.session.add(x)
			db.session.commit()
			if x:
				flash("Post Saved Successfully")
			return redirect(url_for('edit_post', post_slug = form.title.data))

	return render_template('admin_edit.html', page_title = 'New Post', form = form)



@app.route('/admin/edit/<post_slug>', methods = ['GET', 'POST'])
@login_required
def edit_post(post_slug):
	post = Post.query.filter(func.lower(Post.title) == func.lower(post_slug)).first()
	
	if post == None:
		return "404"

	form = EditPost()
	if request.method == 'POST':
		if request.form['submit'] == 'Publish' and form.validate_on_submit():
			print post.publish_date
			if post.publish_date == None:
				post.publish_date = datetime.datetime.now()
			post.title = form.title.data
			post.content = form.content.data
			post.tags = form.tags.data
			db.session.commit()
			return redirect(url_for('admin'))
		elif request.form['submit'] == 'Save Draft' and form.validate_on_submit():
			if post.publish_date != None:
				post.publish_date = None
			post.title = form.title.data
			post.content = form.content.data
			post.tags = form.tags.data
			db.session.commit()
			return redirect(url_for('admin'))

	form.title.data = post.title
	form.content.data = post.content
	form.tags.data = post.tags
	return render_template('admin_edit.html', page_title = 'Edit Post', form = form)


@app.route('/admin/delete/<post_slug>', methods = ['GET', 'POST'])
@login_required
def delete_post(post_slug):
	post = Post.query.filter(func.lower(Post.title) == func.lower(post_slug)).first()
	if post == None:
		return "404"

	db.session.delete(post)
	db.session.commit()

	return redirect(url_for('admin'))



@app.route('/upload', methods=['POST'])
@login_required
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			now = datetime.datetime.now()
			filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))

			actual_filename = os.path.join( main_path + filename)
			
			file.save(actual_filename) 
			return jsonify({"filename": filename,
				"success":True})

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/admin/update_info', methods=['GET', 'POST'])
@login_required
def update_info():
	form = EditInfo()


	if request.method == 'POST':
		g.info.title = form.title.data
		g.info.description = form.description.data
		g.info.cover_image = request.form['cover_image']
		g.info.cover_color = request.form['cover_color']
		g.info.cover_height = request.form['cover_height']
		g.info.header_color = request.form['header_color']
		g.info.website_link = form.website_link.data
		g.info.twitter_link = form.twitter_link.data
		g.info.facebook_link = form.facebook_link.data
		db.session.commit()

	form.title.data = g.info.title
	form.description.data = g.info.description
	form.website_link.data = g.info.website_link
	form.cover_height = g.info.cover_height
	form.cover_color = g.info.cover_color
	form.twitter_link.data = g.info.twitter_link
	form.facebook_link.data = g.info.facebook_link

	return render_template('update.html', page_title = 'Edit Info', form = form)
