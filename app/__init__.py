import os, config

from flask import Flask, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import flask_login


app=Flask(__name__)
Bootstrap(app)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
manager.add_command('db', MigrateCommand)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



from app import views
from app.models import User, Rating
from app.seeds import Faker

manager.add_command("seed", Faker())
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

def app_run():
    manager.run()
    
