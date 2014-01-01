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

#class ChildPage(db.Model):
#	id = db.Column(db.Integer, primary_key = True)
#	page = db.Column(db.String(80))
#	parent = db.Column(db.String, nullable = False)
#	parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
#	parent = db.relationship('Parent', backref=db.backref('children', lazy='dynamic'))

#	content = db.Column(db.UnicodeText)

	
#	def get_id(self):
#		return unicode(self.id)
#
#	def __repr__(self):
#		return 	self.page


#######################################
#									  #		
#			ARCHIVE MODEL			  #
#									  #
#######################################

# Create models
#class Branch(db.Model):
#	id = db.Column(db.Integer, primary_key = True)
#	name = db.Column(db.String(120))

#	def __repr__(self):
#		return (self.name)

#class Status(db.Model):
#	id = db.Column(db.Integer, primary_key = True)
#	status = db.Column(db.String(120), nullable = False)

#	def __repr__(self):
#		return (self.status)


#class Sessions(db.Model):
#	id = db.Column(db.Integer, primary_key = True)
#	month = db.Column(db.String(120), nullable = False)
#
#	def __repr__(self):
#		return (self.month)


#class Archive(db.Model):

#	id = db.Column(db.Integer, primary_key=True)
#	name = db.Column(db.Unicode(64), nullable = False)
#	session = db.Column(db.String, nullable = False)
#	session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
#	session = db.relationship('Sessions', backref=db.backref('children', lazy='dynamic'))
    
#	year = db.Column(db.Integer, nullable = False)
#	__table_args__ = (db.CheckConstraint(year >= 2000, name='check_bar_positive'),{})

#	branch = db.Column(db.String, nullable = False)
#	branch_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
#	branch = db.relationship('Parent', backref=db.backref('archive_children', lazy='join'))

#	status = db.Column(db.String, nullable = False)
#	status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
#	status = db.relationship('Status', backref=db.backref('children', lazy='join'))

#	description = db.Column(db.UnicodeText, nullable = False)

#	def __repr__(self):
#		return (self.name)


#class LocationImage(db.Model):
#	id = db.Column(db.Integer, primary_key=True)
#	member_name = db.Column(db.String(128))
#	path = db.Column(db.String(64))

#	location_id = db.Column(db.Integer, db.ForeignKey(Archive.id))
#	location = db.relation(Archive, backref='images')

