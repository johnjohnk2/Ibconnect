from datetime import datetime
from sqlalchemy import desc
from Ibconnect import db

from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from threading import Thread
import  queue, time


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date= db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)
    
    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120),unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


class TestWrapper(EWrapper):
    def init_time(self):
        time_queue = queue.Queue()
        self._time_queue = time_queue
        return time_queue

    def currentTime(self, time_from_server):
        self._time_queue.put(time_from_server)

class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def retrieve_time(self):
        print("\n Getting the time from the server... ")
        time_storage = self.wrapper.init_time()
        self.reqCurrentTime()
        return time_storage.get()

class TestApp(TestWrapper, TestClient):
    def __init__(self, ipaddress, portid, clientid):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper = self)
        
        self.connect(ipaddress, portid, clientid)
        
        thread = Thread(target = self.run)
        thread.start()
        setattr(self, "_thread", thread)