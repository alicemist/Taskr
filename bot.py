import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask , request , Response 
from slackeventsapi import SlackEventAdapter
import requests



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
    
    if BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1

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
def addtask():

    text = request.form.get("text")
    print(text)
    response = requests.post(os.environ['XANOTASK']  # need to be dynmaic values from user.
    , data = {"Task": text}
    
)
    client.chat_postMessage(channel='#general' , text=f"Okay I am adding new task: {text}")
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
