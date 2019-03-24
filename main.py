import logging
import os
import re
from six.moves.urllib.request import urlopen

from flask import Flask
from flask_ask import Ask, request, session, question, statement, context
from web_md_functions import get_drug_summary

import sqlite3
conn = sqlite3.connect("storage.db")

c = conn.cursor()

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def createTables():
    # Create table
    c.execute("CREATE TABLE if not exists users (firstName text, secondName text, amazonID text, userID INTEGER PRIMARY KEY AUTOINCREMENT)")
    c.execute("CREATE TABLE if not exists drugAllocations (userID INTEGER, slotNumber INTEGER, inUse INTEGER, drugName TEXT, drugQuantity INTEGER, dose INTEGER, morning INTEGER, lunch INTEGER, evening INTEGER )")
    c.execute("CREATE TABLE if not exists drugHistory (userID INTEGER, date TEXT, drugName TEXT, dose INTEGER)")
    conn.commit()

createTables()

@ask.launch
def launch():
    speech_output = "Hey, I'm your personal nurse, what do you want to know? You can say 'can I have my pills', 'tell me about paracetamol', 'what are the side effects of ibuprofen', and so much more."
    reprompt_text = "Hey, I'm pilly, what do you want to know?"
    return question(speech_output).reprompt(reprompt_text)


@ask.intent("DrugInformationIntent", convert={ "DrugName": "DrugName" })
def DrugInformationIntentHandler(DrugName):
    print("Drug: " + DrugName)
    print(context.System.user.userId)
    info = get_drug_summary(DrugName, "uses")
    if(not info):
        return statement("Sorry, I couldn't find " + DrugName + " on WebMD")
    else:
        return statement("WebMD says " + info)

@ask.intent("DrugSideEffectsIntent", convert={ "DrugName": "DrugName" })
def DrugSideEffectsHandler(DrugName):
    print("Drug: " + DrugName)
    info = get_drug_summary(DrugName, "side effects")
    if(not info):
        return statement("Sorry, I couldn't find " + DrugName + " on WebMD")
    else:
        return statement("From WebMD on the side effects of " + DrugName + ", " + info)

@ask.intent("DrugPrecautionsIntent", convert={ "DrugName": "DrugName" })
def DrugPrecautionsHandler(DrugName):
    print("Drug: " + DrugName)
    info = get_drug_summary(DrugName, "precautions")
    if(not info):
        return statement("Sorry, I couldn't find " + DrugName + " on WebMD")
    else:
        return statement("From WebMD on precautions when taking " + DrugName + ", " + info)

@ask.intent("DrugInteractionsIntent", convert={ "DrugName": "DrugName" })
def DrugInteractionsHandler(DrugName):
    print("Drug: " + DrugName)
    info = get_drug_summary(DrugName, "interactions")
    if(not info):
        return statement("Sorry, I couldn't find " + DrugName + " on WebMD")
    else:
        return statement("From WebMD on drug interactions with " + DrugName + ", " + info)

@ask.intent("DrugAddIntent", convert={ "DrugName": "DrugName" })
def AddDrugIntentHandler(DrugName):
    c.execute("SELECT userID FROM users WHERE amazonID='" + context.System.user.userId +"'")
    userID = c.fetchone()
    if(not userID):
        print("User not in database! Adding them.")
        c.execute("INSERT INTO users (firstName, secondName, amazonID) VALUES ('Richard', 'Slaney', '" + context.System.user.userId + "')")
        conn.commit()
        c.execute("SELECT userID FROM users WHERE amazonID='" + context.System.user.userId + "'")
        userID = str(c.fetchone()[0])
        for i in range(0, 6):
            c.execute("INSERT INTO drugAllocations VALUES ("+ userID + ", " + str(i) + ", 0, 'None', 0, 0, 0, 0, 0)")
        conn.commit()
    else:
        userID = str(userID[0])
        print("User in database!!!!")
        # c.execute("INSERT INTO drugAllocations ")
    c.execute("SELECT * FROM drugAllocations where userID=" + userID + " AND inUse=0")
    freeSlots = list(c.fetchall())
    print("Number of free drug allocations: " + str(len(freeSlots)))
    conn.commit()
    print(freeSlots)
    if(len(freeSlots) > 0):
        return statement("Added into slot number " + str(freeSlots[0][1]))
    else:
        return statement("No slots to add it into!")

@ask.intent("DispenseDrugsIntent")
def DispenseDrugsIntentHandler():
    c.execute("SELECT userID FROM users WHERE amazonID='" + context.System.user.userId + "'")
    userID = str(c.fetchone()[0])
    c.execute("SELECT * FROM drugAllocations where userID=" + userID)
    drugList = [0]*6
    for drug in c.fetchall():
        if drug[2] == 1:
            drugList[drug[1]] = drug[4]
    print(drugList)
    return statement("Mmmmmmmmmmmmmmmmmmmmmmmmmmm drugs.")

@ask.intent("DispenseDaysDrugsIntent")
def DispenseDaysDrugsIntentHandler():
    return statement("Mmmmmmmmmmmmmmmmmmmmmmmmmmm drugs.")

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Goodbye")

@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement("Goodbye")

@ask.intent("AMAZON.FallbackIntent")
def cancel():
    return question("Sorry, I didn't understand that, what do you want to ask?")

@ask.session_ended
def session_ended():
    return "{}", 200

@app.route("/test")
def test():
    return "<h1>Great success!</h1>"

app.run(debug=False, ssl_context=("cert.pem", "privkey.pem"), port=443, host="0.0.0.0")

conn.close()