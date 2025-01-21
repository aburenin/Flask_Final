import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_assets import Environment, Bundle
from flask_cors import CORS
from flask_login import LoginManager

from Client import GetClient
from Models import db, bcrypt
from Preise import CHECK_PREISE_DB
from Question import CHECK_QUESTION_DB
from portfolio.Portfolio import Gallery

app = Flask(__name__)
app.config.from_object('config')

bcrypt.init_app(app)
db.init_app(app)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

assets = Environment(app)
# Генерация путей к CSS-файлам

css = Bundle(
    os.path.join('css', 'reset.css'),
    os.path.join('css', 'main.css'),
    os.path.join('css', 'footer.css'),
    os.path.join('css', 'navbar.css'),
    os.path.join('css', 'modal.css'),
    os.path.join('css', 'carousel_main.css'),
    os.path.join('css', 'FAQ.css'),
    output=os.path.join('css', 'styles.css'),
    filters='cssmin'
)
assets.register('css_all', css)
with app.app_context():
    assets._named_bundles['css_all'].urls()


@login_manager.user_loader
def load_user(user_id):
    return GetClient(app=app).filter_by(id=user_id)


CORS(app=app)
load_dotenv(find_dotenv())

Gallery.clear_temlates()

# Create new Data Base if not exist and check for changed elements
if not os.path.exists('instance/fotos-baby.db'):
    with app.app_context():
        db.create_all()

CHECK_PREISE_DB(app=app)
CHECK_QUESTION_DB(app=app)
