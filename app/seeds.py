from flask_script import Command
from .models import Rating
from app import db
from random import randint
from time import sleep

class Faker(Command):
    
    def create_ratings(self):
        for r in range(50):
            rating = Rating(operator='10{}'.format(randint(1,5)), queue='400', callerid=''.join(["{}".format(randint(0, 9)) for num in range(0, 11)]), value=randint(1,5))
            # rating = Rating(operator='101'.format(randint(1,5)), queue='400', callerid=''.join(["{}".format(randint(0, 9)) for num in range(0, 11)]), value=randint(1,5))
            print(rating)
            db.session.add(rating)
            db.session.commit()
            sleep(randint(1,5))

    def run(self):
        self.create_ratings()
        print("create faker data rarings")
        
    # operator = db.Column(db.String(20), index=True)
    # queue = db.Column(db.String(20), index=True)
    # callerid = db.Column(db.String(20), index=True)
    # value = db.Column(db.Integer, default=0)
    # created_at = db.Column(db.DateTime(), default=datetime.utcnow)    
