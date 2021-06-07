from __future__ import print_function
from flask import Flask, session
from flask_cors import CORS, cross_origin
from googleapiclient.discovery import build
from google.oauth2 import service_account
from flask_session import Session
import random
import json
import csv



app = Flask(__name__)
cors = CORS(app)

# SESSION_TYPE = 'filesystem'
# app.config.from_object(__name__)

# Session(app)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Ye2opFn9n-of4TSRjWL6Ez61PA4Ioy0BCl8plIg7il0'

service = build('sheets', 'v4', credentials=creds)


#Function Definition
# write sheet to local csv file
def loadFromSheets():
    abcd=sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="sentences!1:1000").execute()
    csv_file = "data/sentence.csv"
    try:
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(abcd['values'])
    except IOError:
        print("I/O error")


# Call the Sheets API
sheet = service.spreadsheets()
loadFromSheets()

def readFromCSV():
    csv_file = "data/sentence.csv"
    try:
        with open(csv_file, 'r') as read_obj: # read csv file as a list of lists
            csv_reader = csv.reader(read_obj) # pass the file object to reader() to get the reader object
            list_of_rows = list(csv_reader) #
            return list_of_rows
    except IOError:
        print("I/O error")


def generateObj(type):
    abcd={}
    abcd['values']=readFromCSV()
    list1=[]
    for i in range(1,len(abcd['values'])):
        dictionary={}
        answers=[]
        resolution=[]
        
        for j in range(0,len(abcd['values'][i])):
            if j>3 and j<13:
                answers.append({'content':abcd['values'][i][j]})
                dictionary['answers']=answers
            elif j>12 and j<16:
                resolution.append(int(abcd['values'][i][j]))
                dictionary['resolution']=resolution
            else:
                dictionary[abcd['values'][0][j]]=abcd['values'][i][j]
        
        if type=='fb' and dictionary['kind']=='single':
            list1.append(dictionary)
        elif type == 'db' and dictionary['kind']=='double':
            list1.append(dictionary)
        elif type == 'tb' and dictionary['kind']=='triple':
            list1.append(dictionary)
        elif type == 'se' and dictionary['kind']=='sentence_equivalence':
            list1.append(dictionary)
        elif type == 'random':
            list1.append(dictionary)
        else:
            continue

    random.shuffle(list1) # to shuffle the list in a random order
    answer=json.dumps(list1)
    return answer


@app.route("/")
def hello():
  return "Hello World!"

@app.route("/load-random-sentences")
def randomSentences():
    answer=generateObj("random")
    return answer

@app.route("/load-random-fb")
def randomSentencesFB():
    answer=generateObj("fb")
    return answer

@app.route("/load-random-db")
def randomSentencesDB():
    answer=generateObj("db")
    return answer
@app.route("/load-random-tb")
def randomSentencesTB():
    answer=generateObj("tb")
    return answer

@app.route("/load-random-se")
def randomSentencesSE():
    answer=generateObj("se")
    return answer

@app.route("/load-config")
def loadConfig():
    loadFromSheets()
    return {"status":"Loaded config successfully"}

if __name__ == "__main__":
  app.run()