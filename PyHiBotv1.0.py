
# coding: utf-8

# In[78]:


import re
import socket
import time
import numpy as np
import requests


# In[79]:


def sleepy(resp):
    time.sleep(resp)


# In[12]:


# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
#CHAN = "#test"                                  # Channelname = #{Nickname}
NICK = "hidrator"                               # Nickname = Twitch username
PASS = "oauth:5p23mgl25n4al4k5txwm5varsue1si"   # www.twitchapps.com/tmi/ will help to retrieve the required authkey
# --------------------------------------------- End Settings -------------------------------------------------------


# In[13]:


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# In[14]:


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!test': command_test,
                   '!asdf': command_asdf}
        if msg[0] in options:
            options[msg[0]]()
# --------------------------------------------- End Helper Functions -----------------------------------------------


# In[36]:


# --------------------------------------------- Start Command Functions --------------------------------------------
def command_test():
    send_message(CHAN, 'tesbta1')


def command_asdf():
    send_message(CHAN, 'asdfster')
    

def command_loop():
    send_message(CHAN, round(np.random.normal()*100,0))
# --------------------------------------------- End Command Functions ----------------------------------------------


# In[93]:


CHAN = ["test","testree", "myth"]  # Channelname = #{Nickname}


# In[97]:


url = "https://api.twitch.tv/helix/streams"
headers = {
    'Authorization': "Bearer 5p23mgl25n4al4k5txwm5varsue1si",
    'User-Agent': "PostmanRuntime/7.20.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "78f0198b-1521-4960-8af3-e3c9f7b98e4c,1b876855-7183-491b-9f62-1366f6be070d",
    'Host': "api.twitch.tv",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }


# In[96]:


while True:
    
    for i in CHAN:
        
        querystring = {"user_login":i}
        response = requests.request("GET", url, headers=headers, params=querystring)
        string = response.text
        s = string[1:len(string)-1].split(", ")
        
        if (len(string) > 30): #if resp txt > 30 then we know the channel is online
            
            con = socket.socket()
            con.connect((HOST, PORT))
            send_pass(PASS)
            send_nick(NICK)
            join_channel(i)
        
            print(i+" is Online")
            send_message('#'+i, round(np.random.normal()*100,0)) #specify the '#' here using the send_msg command
        else:
            print(i+" is Offline")
            
    sleepy(10)


# In[43]:


con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN[i])

data = ""

while True:

    try:
        
        command_loop()
        sleepy(3)

        #data = data+con.recv(1024).decode('UTF-8')
        #data_split = re.split(r"[~\r\n]+", data)
        #data = data_split.pop()

    #    for line in data_split:
    #        line = str.rstrip(line)
    #        line = str.split(line)

     #       if len(line) >= 1:
     #           if line[0] == 'PING':
     #               send_pong(line[1])

      #          if line[1] == 'PRIVMSG':
      #              sender = get_sender(line[0])
      #              message = get_message(line)
      #              parse_message(message)

       #             print(sender + ": " + message)
    
    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")

