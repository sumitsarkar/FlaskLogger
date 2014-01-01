from app import db
from werkzeug import generate_password_hash, check_password_hash

class Info(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String, nullable = False)
	header_color = db.Column(db.String)
	description = db.Column(db.UnicodeText)
	cover_image = db.Column(db.String)
	cover_height = db.Column(db.Integer)
	cover_color = db.Column(db.String)
	website_link = db.Column(db.String)
	twitter_link = db.Column(db.String)
	facebook_link = db.Column(db.String)

	def __init__(self, title, description, cover_image = None, cover_height = None, cover_color = None, header_color = None,  website_link = None, twitter_link = None, facebook_link = None ):
		self.title = title
		self.description = description
		self.cover_image = cover_image
		self.header_color = header_color
		self.website_link = website_link
		self.twitter_link = twitter_link
		self.facebook_link = facebook_link
		self.cover_height = cover_height
		self.cover_color = cover_color

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(80), unique = True)
	pw_hash = db.Column(db.String(100))

	def __init__(self, email="", password=""):
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def is_admin(self):
		if self.perm == 1:
			return True
		else:
			return False

	def __repr__(self):
		return '<User %r>' % self.email

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.Unicode(200), unique = True, nullable = False)
	content = db.Column(db.UnicodeText)
	tags = db.Column(db.Unicode)
	publish_date = db.Column(db.DateTime)

	def __init__(self, title, content, tags = None,  publish_date = None):
		self.title = title
		self.content = content
		self.publish_date = publish_date
	
	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return self.page