import os

from app import app
from app import views
from flask_script import Manager

manager = Manager(app)


if __name__ == '__main__':
    manager.run()

