import time

import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def send(sender, recipient, voltage='NA'):
    # Auth creds file
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        service = build('gmail', 'v1', credentials=creds)
        now = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        message = MIMEText(f'Soil moisture as of {now} is: {voltage}V')
        message['To'] = recipient
        message['From'] = sender
        message['Subject'] = 'Hygrometer update'
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        # Seemingly incorrect method
        # "Message in the body can only be used with an attachment"
        # https://stackoverflow.com/questions/30590988/failed-sending-mail-through-google-api-with-javascript
        create_message = {
            'message': {
                'raw': encoded_message
            }
        }

        # Correct way
        create_message = {
            'raw': encoded_message
        }

        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())

        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


# if __name__ == '__main__':
    # send()