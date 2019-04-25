from datetime import datetime


class Person:
    date_format = '%Y-%m-%d'

    def __init__(self, person):
        self.id = person.get('id')
        self.person = person.get('attributes', {})

    @property
    def first_name(self):
        return self.person.get('first_name')

    @property
    def last_name(self):
        return self.person.get('last_name')

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.person.get('status') == 'active'

    @property
    def birthday(self):
        date = self.person.get('birthdate')
        return self._parse_date(date)

    @property
    def anniversary(self):
        date = self.person.get('anniversary')
        return self._parse_date(date)

    def is_same_day_as_date(self, given_date, date):
        return (
            date.month == given_date.month and
            date.day == given_date.day
        )

    def is_person_birthday(self, date):
        return (
            self.birthday and
            self.is_same_day_as_date(self.birthday, date) and
            self.is_active
        )

    def is_person_anniversary(self, date):
        return (
            self.anniversary and
            self.is_same_day_as_date(self.anniversary, date) and
            self.is_active
        )

    def _parse_date(self, date):
        try:
            return datetime.strptime(date, self.date_format)
        except (ValueError, TypeError):
            return None
