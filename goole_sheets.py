import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import matplotlib.pyplot as plt


      
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


SAMPLE_SPREADSHEET_ID = "Your Googlesheet key"


def get_google_sheets_data():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A1:H3")
            .execute()
        )
        values = result.get("values", [])
        return values
    

    except HttpError as err:
        print(err)
        return None
      
      
data1 = get_google_sheets_data()
data = data1[1:]
def check(name):
  new = None
  for i in range(len(data)):
    if name.title() == data[i][0]:
      new = data[i]
      return new

def generate_pie_chart(present, absent, filename='attendance.jpg'):
    from pathlib import Path
    file_path = Path(filename)
    if file_path.is_file():
        file_path.unlink() 
    labels = 'Present ', 'Absent'
    sizes = [present, absent]
    colors = ['green', 'red']
    plt.figure()
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90)
    plt.axis('equal')
    plt.savefig(filename)
    plt.close()
    return filename
