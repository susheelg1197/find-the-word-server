from __future__ import print_function
from flask import Flask, session
from flask_cors import CORS, cross_origin
from googleapiclient.discovery import build
from google.oauth2 import service_account
from flask_session import Session
import random
import json

app = Flask(__name__)
cors = CORS(app)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

Session(app)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Ye2opFn9n-of4TSRjWL6Ez61PA4Ioy0BCl8plIg7il0'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()




@app.route("/")
def hello():
  return "Hello World!"

@app.route("/load-random-sentences")
def randomSentences():
    abcd =session["result"]
    list1=[]
    for i in range(1,len(abcd['values'])):
        dictionary={}
        for j in range(0,len(abcd['values'][i])):
            dictionary[abcd['values'][0][j]]=abcd['values'][i][j]
        list1.append(dictionary)

    random.shuffle(list1) # to shuffle the list in a random order
    answer=json.dumps(list1)
    return answer

@app.route("/load-config")
def loadConfig():
    session["result"] = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="sentences!1:1000").execute()
    return "Loaded config successfully"

if __name__ == "__main__":
  app.run()