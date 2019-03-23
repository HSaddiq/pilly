import requests
import json

onesignal = {
  "restApiKey" : "NzE3YzlkYWQtZjUwNy00OTZjLTg1ZWUtYzM3MDYzOTM1MWEz",
  "appID" : "5f0aa0ca-04ea-44a2-85c6-bf818caa011e"
}

def sendNotification(title, message):
  payload = { 
    "app_id" : onesignal["appID"],
    "contents" : {"en": message},
    "included_segments" : ["All"],
    "headings" : {"en" : title},
    "small_icon" : "ic_menu_share"
  }

  headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Basic " + onesignal["restApiKey"]
  }
  
  options = {
    "host" : "onesignal.com",
    "port" : 443,
    "path" : "/api/v1/notifications",
    "method" : "POST",
    "headers" : headers
  }
  
  req = requests.post("https://onesignal.com/api/v1/notifications", headers=headers, data=json.dumps(payload))
  
  print(req.status_code, req.reason)



sendNotification("Test message", "Hello there")