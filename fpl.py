import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import requests
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# SPREADSHEET
SAMPLE_SPREADSHEET_ID_input = '1hVuPQVy8-0owGl7KnssQHKs7Brd6Wz46rTkh7OWAtds'
SAMPLE_RANGE_NAME = 'A1:F10'

# FPL ID
FPL_ID = ["899121",
          "584587",
          "1150283" 
          ]

def get_current_data():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sheet_token.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')

    print(values_input)

def crawl_fpl_data():
    # base url for all FPL API endpoints
    base_url = 'https://fantasy.premierleague.com/api/'
    endpoint = "entry/"
    # get data from manager endpoint
    user_data = []
    for id in FPL_ID:
        current_user = []
        # construct url
        full_url_manager = base_url + endpoint + id
        full_url_history = base_url + endpoint + id +"/history"
        
        # get data
        r_manager = requests.get(full_url_manager).json()
        r_history = requests.get(full_url_history).json()
        current_user.append(r_manager)
        current_user.append(r_history)

        user_data.append(current_user)
    
    return user_data

def process_data():
    user_data = crawl_fpl_data()

    print(user_data)


def main():
    process_data()

main()

