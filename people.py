from datetime import datetime
from pytz import timezone

from person import Person
from emails import Email
from pco import PCOClient


class People:

    ANNIVERSARY = 'anniversary'
    BIRTHDAY = 'birthday'

    def __init__(self):
        self.client = PCOClient()

    def special_day_type(self, special_day):
        if special_day == self.BIRTHDAY:
            return 'cumpleaños'
        if special_day == self.ANNIVERSARY:
            return 'aniversario'

    def special_days_people(self, date):
        people = self.client.get_all_people()

        birthdays_people = []
        anniversaries_people = []

        for person_data in people:
            person = Person(person_data)

            if person.is_person_birthday(date):
                birthdays_people.append(person)

            if person.is_person_anniversary(date):
                anniversaries_people.append(person)

        return birthdays_people, anniversaries_people

    def send_emails(self, emails, person, special_day):
        day_type = self.special_day_type(special_day)
        email = Email(
            'birthdays@hillsong.es',
            emails,
            day_type.capitalize(),
            f'Hoy es el {day_type} de {person.name}. Emails: {emails}'
        )

        return email.send_email()

    def check_people_specials_days(self, date, send_email=True):
        birthdays_people, anniversaries_people = self.special_days_people(date)

        for person in birthdays_people:
            emails = self.client.person_leaders_emails(person)
            print(f'Send birthday email for {person.name} to {emails}')
            if send_email:
                response = self.send_emails(emails, person, self.BIRTHDAY)
                print(f'Email: {response.status_code}')

        for person in anniversaries_people:
            emails = self.client.person_leaders_emails(person)
            print(f'Send anniversary email for {person.name} to {emails}')
            if send_email:
                self.send_emails(emails, person, self.ANNIVERSARY)
                print(f'Email: {response.status_code}')

        return birthdays_people, anniversaries_people
