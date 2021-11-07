## utilize sample code
## https://developers.google.com/sheets/api/quickstart/python#step_2_configure_the_sample

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import folium

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# apitest/銭湯
# https://docs.google.com/spreadsheets/d/1Sj4mk1njb50PvkT3t9tH0INyY6ilGbeuveyf_41VA8A
SAMPLE_SPREADSHEET_ID = '1Sj4mk1njb50PvkT3t9tH0INyY6ilGbeuveyf_41VA8A'
SAMPLE_RANGE_NAME = '銭湯!A2:I'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])


    home = values[0]
    location = [home[2],home[3]]
    folium_map = folium.Map(location,zoom_start=12)

    # Home Marker
    folium.Marker(location,
                  popup="自宅",
                  icon=folium.Icon(color='red')
    ).add_to(folium_map)

    public_baths_info = values[1:-1]

    if not values:
        print('No data found.')
    else:
        for public_bath_info in public_baths_info:
            # Print columns A and E, which correspond to indices 0 and 4.
            location = [public_bath_info[2],public_bath_info[3]]

            # https://gis.stackexchange.com/questions/385565/inserting-an-url-link-in-markers-popup-in-folium

            url = public_bath_info[8:9]

            tooltip = public_bath_info[1]

            if url:
                #popup= "<a href=https://fr.wikipedia.org/wiki/Place_Guillaume_II>Place Guillaume II</a>"
                popup = "<a href=" + url[0] + ">" + public_bath_info[1] + "</a>"
            else:
                popup = public_bath_info[1]

            print(popup)
            folium.Marker(location,
                          popup=popup,
                          tooltip=tooltip).add_to(folium_map)

    folium_map.save('public_bath.html')

if __name__ == '__main__':
    main()
