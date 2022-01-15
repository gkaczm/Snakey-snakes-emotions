from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_emails(index: int):
    creds = None

    if os.path.exists('google/token.pickle'):
        with open('google/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('google/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().list(userId='me').execute()

    msg = result.get('messages')[index]

    txt = service.users().messages().get(userId='me', id=msg['id']).execute()

    try:
        payload = txt['payload']
        headers = payload['headers']

        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']

        parts = payload.get('parts')[0]
        data = parts['body']['data']
        data = data.replace("-", "+").replace("_","/")
        decoded_data = base64.b64decode(data)

        soup = BeautifulSoup(decoded_data, "lxml")
        body = soup.body()

        print("Subject: ", subject)
        print("From: ", sender)
        print("Message: ", str(body[0].text))

        return {
            "subject": subject,
            "from": sender,
            "message": str(body[0].text)
        }
    except Exception as e:
        print(e)
        pass
