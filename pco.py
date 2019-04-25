import json
import requests
from requests.auth import HTTPBasicAuth

from environs import Env

env = Env()


class PCOClient:
    BASE_URL = 'https://api.planningcenteronline.com/{app}/v2'

    def __init__(self):
        app_id = env('PCO_APP_ID')
        secret = env('PCO_SECRET')
        self.basic_auth = HTTPBasicAuth(app_id, secret)

    def page_is_valid(self, response, content):
        return response.status_code >= 200 and\
            response.status_code < 400 and\
            content.get('data')

    def check_response(self, response, content):
        if not self.page_is_valid(response, content):
            print(f'{response.url} ({response.status_code})')
            print(f'  {content}')
            print(f'Something went wrong: {response.status_code}')

    def make_request(self, url):
        response = requests.get(url, auth=self.basic_auth)
        try:
            content = json.loads(response.content)
        except json.decoder.JSONDecodeError:
            # Ignore the error, for printing it on check_response
            content = response.content
        self.check_response(response, content)

        return response, content

    def make_paginated_request(self, url):
        response, content = self.make_request(url)

        data = content.get('data')
        next_url = content['links'].get('next')

        return data, next_url

    def make_simple_request(self, url):
        response, content = self.make_request(url)
        return content.get('data')

    def get_all_people(self, per_page=100, offset=0):
        app_url = self.BASE_URL.format(app='services')
        people_url = f'{app_url}/people?per_page={per_page}&offset={offset}'

        people = []

        while people_url:
            data, people_url = self.make_paginated_request(people_url)
            people += data

        return people

    def services_person_teams(self, person):
        app_url = self.BASE_URL.format(app='services')
        person_teams_url = f'{app_url}/people/{person.id}/teams'
        return self.make_simple_request(person_teams_url)

    def services_team_leaders(self, team_id):
        app_url = self.BASE_URL.format(app='services')
        team_leaders_url = f'{app_url}/teams/{team_id}/team_leaders'
        return self.make_simple_request(team_leaders_url)

    def people_person_emails(self, person_id):
        app_url = self.BASE_URL.format(app='people')
        leaders_url = f'{app_url}/people/{person_id}/emails?order=-updated_at'
        return self.make_simple_request(leaders_url)

    def person_email(self, person_id):
        emails = self.people_person_emails(person_id)
        if len(emails) > 0:
            return emails[0]['attributes']['address']

    def person_leaders_emails(self, person):
        teams = self.services_person_teams(person)
        teams_ids = [team['id'] for team in teams]

        leaders_emails = []
        for team_id in teams_ids:
            leaders = self.services_team_leaders(team_id)
            for leader in leaders:
                leader_id = leader['relationships']['person']['data']['id']
                leader_email = self.person_email(leader_id)
                if leader_email:
                    leaders_emails.append(leader_email)

        return set(leaders_emails)
