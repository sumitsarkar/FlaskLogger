import os
from flask import Flask, render_template, g, url_for
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.misaka import Misaka


from sqlalchemy import func
from config import basedir

app = Flask(__name__)
Misaka(app, autolink = True, strikethrough = True, superscript = True, fenced_code = True)

main_path = os.path.join(os.path.dirname(__file__))

path = os.path.join(os.path.dirname(__file__), 'static')


app.config.from_object('config')


app.jinja_env.add_extension('jinja2.ext.do')

db = SQLAlchemy(app)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models, forms

print path
