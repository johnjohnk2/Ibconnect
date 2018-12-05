#! /usr/bin/env python

from Ibconnect import app, db
from Ibconnect.models import User, TestWrapper,TestClient, TestApp
from flask_script import Manager, prompt_bool



manager = Manager(app)

@manager.command
def initdb():
        db.create_all()
        db.session.add(User(username="Jonathan", email="Jonathan.@example.com"))
        db.session.add(User(username="Szalavecz", email="Szalavecz.@example.com"))
        db.session.commit()
        print ('Initialized the database')

@manager.command
def dropdb():
    if prompt_bool( 
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print ('Dropped the database')

if __name__ =='__main__':
    manager.run()
    manager = TestApp("127.0.0.1", 7496, 0)
    current_time = app.retrieve_time()
    print(time.ctime(current_time))
    manager.disconnect()