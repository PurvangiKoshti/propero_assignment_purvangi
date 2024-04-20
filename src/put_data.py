import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

class ScrapeData:
    """
    A class for writing data into a Google Sheet.
    """

    def get_credentials_token(self):
        """
        Retrieves or refreshes credentials token for accessing Google Sheets API.
        """
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('sheets', 'v4', credentials=creds)

    def write_in_google_sheet(self, data):
        """
        Writes data into a specified Google Sheet.

        Args:
            data (list): A list of dictionaries containing data to be written.
        """
        self.get_credentials_token()

        values = [["Title", "Date", "Description", "Image link", "Anchor link"]]
        for entry in data:
            values.append([entry["title"], entry["date"], entry["description"], entry["image_link"], entry["anchor_link"]])

        range_name = f'Sheet1!A1:{chr(ord("A") + len(values[0]) - 1)}{len(values)}'

        body = {'values': values}
        spreadsheet_id = "12Bb_UE2nzr3dT4MlnjahcpDC9v8hXud1VxlcRg_mZIA"
        result = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='RAW', body=body).execute()
        
        print('{0} cells updated.'.format(result.get('updatedCells')))

