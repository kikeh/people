import sendgrid
from environs import Env

env = Env()


class Email:
    _default_emails = env('DEFAULT_EMAILS').split(',')
    _api_key = env('SENDGRID_API_KEY')

    def __init__(self, sent_from, to, subject, body):
        self.sent_from = sent_from
        self.to = to
        self.subject = subject
        self.body = body

    def _start_server(self):
        try:
            server = sendgrid.SendGridAPIClient(apikey=self._api_key)
            return server
        except Exception as e:
            raise Exception(f'Something went wrong: {e}')

    def _prepare_data(self):
        data = {
            "personalizations": [
                {
                    "to": [{"email": email} for email in self._default_emails],
                    "subject": self.subject,
                }
            ],
            "from": {
                "email": self.sent_from,
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": self.body,
                }
            ]
        }
        return data

    def send_email(self):
        server = self._start_server()
        data = self._prepare_data()

        return server.client.mail.send.post(request_body=data)
