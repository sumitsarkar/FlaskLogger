from flask.ext.wtf import Form, TextField, PasswordField, SubmitField, TextAreaField, TextArea
from flask.ext.wtf import Required, Email, Length

from wtforms import TextField, BooleanField
from wtforms.fields.html5 import EmailField, DateField, URLField
from wtforms.validators import Required, email, url
from models import User
from flask import g, session

#class SignUpForm(Form):
#	email = EmailField('Email Address', validators = [email()])
#	password = PasswordField('Password', validators = [Required('Please enter a valid password between 8 and 30 characters.'), Length(min = 8, max = 30)])
#	submit = SubmitField('Create Account')
#
#	def __init__(self, *args, **kwargs):
#		Form.__init__(self, *args, **kwargs)
#
#	def validate(self):
#		if not Form.validate(self):
#			return False
#		user = self.get_user()
#		if user:
#			self.email.errors.append("That email is already taken.")
#			return False
#		else:
#			return True
#
#	def get_user(self):
#		return User.query.filter_by(email = self.email.data.lower()).first()

class LogInForm(Form):
	email = EmailField('Email Address', validators = [email()])
	password = PasswordField('Password', validators = [Required('Password field cannot remain empty.')])
	submit = SubmitField('Login')

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = self.get_user()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid email or password.")
			return False

	def get_user(self):
		return User.query.filter_by(email = self.email.data.lower()).first()
	

class EditPost(Form):
	title = TextField('Title', validators = [Required('Title field cannot remain empty.')])
	content = TextAreaField('Enter your markdown')
	tags = TextField('Tags')
	publish = SubmitField('Publish')
	draft = SubmitField('Save Draft')


class EditInfo(Form):
	title = TextField('Site Title', validators = [Required('Title field cannot remain empty.')])
	cover_image = TextField('Cover Image Link')
	description = TextAreaField('Description')
	website_link = URLField('Website URL', validators = [url()])
	twitter_link = TextField('Twitter Username')
	facebook_link = TextField('Facebook Username')

