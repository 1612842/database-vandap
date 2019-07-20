from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import create_engine
from sqlalchemy.sql import text

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    avatar = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=0 ,nullable=False)

class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)
    receiver_type = db.Column(db.String, nullable=False)
    message_time = db.Column(db.DateTime,nullable = False, default=datetime.datetime.utcnow)
    message_content = db.Column(db.String, nullable=False)