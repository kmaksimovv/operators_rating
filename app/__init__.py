import os, config

from flask import Flask, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import flask_excel as excel
from flask_bootstrap import Bootstrap

app=Flask(__name__)
Bootstrap(app)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
manager.add_command('db', MigrateCommand)

excel.init_excel(app)

from app import views
from app import models
from app.seeds import Faker

manager.add_command("seed", Faker())


def app_run():
    manager.run()
    
