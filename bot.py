from msilib import datasizemask
from turtle import delay
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask , request , Response ,jsonify
from slackeventsapi import SlackEventAdapter
import requests
import json
import time
from threading import Thread



env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

#client.chat_postMessage(channel='#general' , text="Hello I am you!")
BOT_ID = client.api_call("auth.test")['user_id']
message_counts = {} 
# Echoes message to user who sends 
@slack_event_adapter.on('message')   
def message(payload):
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
     
    #client.chat_postMessage(channel='#general' , text=text)
#message count
# @app.route('/messagecount' , methods=['POST'])
# def message_count():
#     data = request.form
#     print(data)
#     user_id = data.get('user_id')
#     message_count = message_counts.get(user_id,0)
#     client.chat_postMessage(channel='#general' , text=f"Messages: {message_counts}")
#     return Response(), 200

#add Project   
@app.route('/addproject' , methods=['POST'])
def addproject():
    text = request.form.get("text")
    while text != "" :  #waiting for user input 
        client.chat_postMessage(channel='#general' , text=f"Okay I am creating new Project: {text}")
        response = requests.post(os.environ['XANOPROJECT']  # need to be dynmaic values from user.
        , data = {"Project_Name": text}
     
)
        if  response.status_code == 200:
            print("status code received. breaking loop..." )
            break

    if text == "":

        client.chat_postMessage(channel='#general' , text="Please enter a Project Name ater /addproject.")


    
    return Response(), 200
    


#add task   
@app.route('/addtask' , methods=['POST'])
def commandaddtask(task):
    text = request.form.get("text")
    client.chat_postMessage(channel='#general' , text="Is this project personal?") 
    


# def addtask(text):


    
def projectlist():
    
    projects = requests.get(os.environ['XANOPROJECT'])
    parseddata = json.loads(projects.content)
    client.chat_postMessage(channel='#general' , text=f"you have {len(parseddata)} projects...")
    time.sleep(1)
    client.chat_postMessage(channel='#general' , text="...")
    for i in range(len(parseddata)):
        
        Projectlist= []
        Projectlist = parseddata[i]["Project_Name"],parseddata[i]["id"]
        

        client.chat_postMessage(channel='#general' , text=f"{Projectlist}") 
        Projectlist= []
    time.sleep(1)
    client.chat_postMessage(channel='#general' , text="You can add tasks to projects with specifing id of the project with /addtask command.")
# if "yes" in text.lower():
#             response = requests.post(os.environ['XANOTASK'], data = {"Task": text,"slackbotprojectinfo_id": id } ) 
@app.route('/listproject' , methods=['POST','GET'])
def listproject():

    thr = Thread(target=projectlist)
    thr.start()

    return      client.chat_postMessage(channel='#general' , text="lets look at projects..") 
    
        # client.chat_postMessage(channel='#general' , text="Please specify the id of the project") 
        
 
        
        # id = request.form.get("text")
        # if id != "" :

        #     response = requests.post(os.environ['XANOTASK'], data = {"Task": var_text,"slackbotprojectinfo_id": id } )              







    return Response(), 200 

# #UpdateTask  
# @app.route('/updatetask' , methods=['POST'])
# def post():
#     text = request.form.get("text")
#     print(text)
#     response = requests.post(os.environ['XANO']  # dynmaic values from user.
#     , data = {"Task": text}
    
# )
#     client.chat_postMessage(channel='#general' , text=f"Okay I am adding new task: {text}")
#     return Response(), 200   


if __name__ == "__main__":
    app.run(debug=True)
