"""OpenAQ Air Quality Dashboard with Flask."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import openaq

api = openaq.OpenAQ()
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(200))
    value = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return f'[Id: {self.id} | Time: {self.datetime} | Value: {self.value}]'


def get_results():
    api = openaq.OpenAQ()
    foo, bar = api.measurements(city='Los Angeles', parameter='pm25')
    ls = []
    for value in range(0, len(bar['results'])):
        val = (
            bar['results'][value]['date']['utc'],
            bar['results'][value]['value'])
        ls.append(val)
    return ls


@APP.route('/')
def root():
    """Base view."""

    return str(Record.query.filter(Record.value >= 10).all())


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    data = get_results()
    date = [a for a, b in data]
    val = [b for a, b in data]
    last_id = -1
    for v in range(0, len(data)):
        last_id += 1
        rec = Record(id=last_id, datetime=str(date[v]), value=int(val[v]))
        DB.session.add(rec)
    DB.session.commit()
    return 'Data refreshed!'
