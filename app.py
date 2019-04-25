from datetime import datetime
from pytz import timezone

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from people import People


app = Flask(__name__)


def special_days_with_date(month=None, day=None, send_email=False):
    people = People()
    date = datetime.now(timezone('Europe/Madrid'))

    if all([month, day]):
        date = datetime(date.year, int(month), int(day))

    if not send_email:
        birthdays_people, anniversaries_people =\
            people.special_days_people(date)
    else:
        birthdays_people, anniversaries_people =\
            people.check_people_specials_days(date)

    return render_template(
        'people.html',
        date=date,
        birthdays=birthdays_people,
        anniversaries=anniversaries_people,
    )


@app.route("/")
def index():
    return "OK"


@app.route("/check_special_days/")
def check_special_days():
    return special_days_with_date(send_email=False)


@app.route("/check_special_days/<month>/<day>")
def check_special_days_with_date(month, day):
    return special_days_with_date(month, day)


def _external_call_days():
    people = People()
    date = datetime.now(timezone('Europe/Madrid'))
    people.check_people_specials_days(date)


Bootstrap(app)
