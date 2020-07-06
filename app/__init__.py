import os, config
import chartkick

from flask import Flask, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
manager.add_command('db', MigrateCommand)

from app import views
from app import models
from app.seeds import Faker

manager.add_command("seed", Faker())


def app_run():
    manager.run()
    
