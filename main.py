import logging
import os
import re
from six.moves.urllib.request import urlopen

from flask import Flask
from flask_ask import Ask, request, session, question, statement
from web_md_functions import get_drug_summary

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
    speech_output = "Hey, I'm pilly, what do you want to know?"
    reprompt_text = "Hey, I'm pilly, what do you want to know?"
    return question(speech_output).reprompt(reprompt_text)


@ask.intent("DrugInformationIntent", convert={ "DrugName": "DrugName" })
def DrugInformationIntentHandler(DrugName):
    print("Drug: " + DrugName)
    return statement("WebMD says " + get_drug_summary(DrugName, "uses"))

@ask.intent("DrugSideEffectsIntent", convert={ "DrugName": "DrugName" })
def DrugSideEffectsHandler(DrugName):
    print("Drug: " + DrugName)
    return statement("From WebMD on the side effects of " + DrugName + ", " + get_drug_summary(DrugName, "side effects"))

@ask.intent("DrugPrecautionsIntent", convert={ "DrugName": "DrugName" })
def DrugPrecautionsHandler(DrugName):
    print("Drug: " + DrugName)
    return statement("From WebMD on precautions when taking " + DrugName + ", " + get_drug_summary(DrugName, "precautions"))

@ask.intent("DrugInteractionsIntent", convert={ "DrugName": "DrugName" })
def DrugInteractionsHandler(DrugName):
    print("Drug: " + DrugName)
    return statement("From WebMD on drug interactions with " + DrugName + ", " + get_drug_summary(DrugName, "interactions"))

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

app.run(debug=False, ssl_context=("cert.pem", "privkey.pem"), port=443, host="0.0.0.0")