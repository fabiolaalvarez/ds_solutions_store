"""
Unit test uploaded to Code Grader for Sprint Challenge 3.
"""
from random import randint
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from aq_dashboard import refresh, get_results, Record, root, DB, API

# Creating testing application to compare results
APP_TEST = Flask(__name__)
APP_TEST.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite3'
APP_TEST.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB_TEST = SQLAlchemy(APP_TEST)

# connecting to API
API_TEST = openaq.OpenAQ()

# Test example data
result_test_1 = ('3000-12-11T18:00:00Z', 145124151)
result_test_2 = ('3000-12-11T16:00:00Z', 234059823)
result_test_3 = ('3000-12-11T17:00:00Z', 832745322)


def test_get_results():
    """
    Testing get_results() - Testing recent results that come directly
    from the API. Will contain 100 observations.
    """
    results = get_results()
    results_tester = get_results_tester()
    assert results == results_tester


def test_refresh_route():
    """
    Testing app.route('refresh/') - Test the string output we get from
    refresh.
    """
    refreshed_string = refresh()
    records = Record.query.all()

    refresh_tester()
    records_tester = RecordTester.query.all()

    assert "refreshed" in refreshed_string.lower()
    assert len(records) == len(records_tester)

    # asserting that every result from returned list is identical to our refresh_tester
    for record, record_tester in zip(records, records_tester):
        print(record)
        print(record_tester)
        assert record.value == record_tester.value
        assert record.datetime == record_tester.datetime


def test_root_route():
    """
    Testing app.route('/') - Test that the newest output is being returned
    when we enter the root route of the application.
    """
    assert isinstance(root(), str)
    assert root() == root_tester()


def test_database():
    """
    Testing Database and Record Table - Check to make sure test results are properly added to the database
    and the proper column types and names were used.

    DataBase Test Points:
    result_test_1 = ('3000-12-11T18:00:00Z', 145124151)
    result_test_2 = ('3000-12-11T16:00:00Z', 234059823)
    result_test_3 = ('3000-12-11T17:00:00Z', 832745322)
    """
    # DEVELOPMENT - clearing databases from test to prevent duplicates for mocks
    DB_TEST.drop_all()
    DB_TEST.create_all()

    # Adding result_testers to DB
    record_1 = Record(datetime=result_test_1[0], value=result_test_1[1])
    record_2 = Record(datetime=result_test_2[0], value=result_test_2[1])
    record_3 = Record(datetime=result_test_3[0], value=result_test_3[1])
    DB.session.add(record_1)
    DB.session.add(record_2)
    DB.session.add(record_3)

    # Adding result_testers to DB_TEST
    record_test_1 = RecordTester(
        datetime=result_test_1[0], value=result_test_1[1])
    record_test_2 = RecordTester(
        datetime=result_test_2[0], value=result_test_2[1])
    record_test_3 = RecordTester(
        datetime=result_test_3[0], value=result_test_3[1])
    DB_TEST.session.add(record_test_1)
    DB_TEST.session.add(record_test_2)
    DB_TEST.session.add(record_test_3)

    DB.session.commit()
    DB_TEST.session.commit()

    # Making sure database has correct columns
    assert isinstance(Record.id, type(RecordTester.id))
    assert isinstance(Record.datetime, type(RecordTester.datetime))
    assert isinstance(Record.value, type(RecordTester.value))

    # Querying result_testers from database
    grab_result_test_1 = Record.query.filter(
        Record.value == 145124151).all()[0]
    grab_result_test_2 = Record.query.filter(
        Record.value == 234059823).all()[0]
    grab_result_test_3 = Record.query.filter(
        Record.value == 832745322).all()[0]

    # Querying result_testers from test database
    grab_result_test_1_tester = RecordTester.query.filter(
        RecordTester.value == 145124151).all()[0]
    grab_result_test_2_tester = RecordTester.query.filter(
        RecordTester.value == 234059823).all()[0]
    grab_result_test_3_tester = RecordTester.query.filter(
        RecordTester.value == 832745322).all()[0]

    # Making sure datetime is correct
    assert grab_result_test_1.datetime == grab_result_test_1_tester.datetime
    assert grab_result_test_2.datetime == grab_result_test_2_tester.datetime
    assert grab_result_test_3.datetime == grab_result_test_3_tester.datetime

    # Making sure value is correct
    assert grab_result_test_1.value == grab_result_test_1_tester.value
    assert grab_result_test_2.value == grab_result_test_2_tester.value
    assert grab_result_test_3.value == grab_result_test_3_tester.value


# Functions for testing
def root_tester():
    return str(Record.query.filter(Record.value >= 10).all())


def refresh_tester():
    DB_TEST.drop_all()
    DB_TEST.create_all()
    for result in get_results_tester():
        record = RecordTester(datetime=result[0], value=result[1])
        DB_TEST.session.add(record)
    DB_TEST.session.commit()


def get_results_tester():
    _, body = API_TEST.measurements(city='Los Angeles', parameter='pm25')
    results = []
    for result in body['results']:
        results.append((result['date']['utc'], result['value']))
    return results


class RecordTester(DB_TEST.Model):
    id = DB_TEST.Column(DB_TEST.Integer, primary_key=True)
    datetime = DB_TEST.Column(DB_TEST.String(25))
    value = DB_TEST.Column(DB_TEST.Float, nullable=False)

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value)
