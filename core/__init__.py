from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
engine = create_engine ('postgresql://mono@localhost/mono')
db = scoped_session(sessionmaker(bind=engine))

app.config['SECRET_KEY'] = 'sgfa23/>"?!:@><//werwert'

from core import routes