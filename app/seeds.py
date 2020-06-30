from flask_script import Command
from .models import Rating
from app import db

class Faker(Command):
    def run(self):
        print("Fake data entered!!!")
        r1 = Rating(operator='101', queue='400', callerid='7845995050', opinion='4')
        db.session.add(r1)
        db.session.commit()

    # operator = db.Column(db.String(20), index=True)
    # queue = db.Column(db.String(20), index=True)
    # callerid = db.Column(db.String(20), index=True)
    # opinion = db.Column(db.String(1))
