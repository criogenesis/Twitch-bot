import discord  
import os.path
import json
import asyncio
import sys
import csv
logfile = "logger_file.txt"
keywords = ["date","time","user","msg"]
client = discord.Client()
print(os.path.isfile(logfile))
print(sys.version)
@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('ready!')
    


@client.async_event
def on_message(message):
    if message.author == client.user:
        return
    if message.content not in "!logopen":
        RowDict = {}
        for key in keywords:
            RowDict[key] = ""
        for key,value in RowDict.items():
            print(key, value)
        if not os.path.isfile(logfile):
            logger_list = []
        
        else:
            with open(logfile, "r") as logger_file:
                logger_list = json.load(logger_file)
            
            timem = message.timestamp
            timems = str(timem)
            print(timems)
            hourdis = timems.split(':')
            seconds = hourdis[1]
            #print(hourdis)
            hourdism = hourdis[0].split(' ')
            Thedate = hourdism[0]
            Thehour = hourdism[1]
            Thehouri = int(Thehour)
            Thehour = Thehouri - 5
            Thehour = str(Thehour)
            #print(Thehour)
            #print(type(Thehouri))
            Thetime = (Thehour + ':' + seconds)
            Theuser = (message.author.name)
            Thepreform = ('At ' + Thetime + ' on ' + Thedate + ', ' + Theuser + ' said')
            print(Thepreform)
            #print(Thetime + ',', Thedate)
            
            
        logger_list.append(message.content)
        print(logger_list)
        with open(logfile, "w") as logger_file:
            json.dump(logger_list, logger_file)
    if message.content.startswith("!logopen"):
        with open(logfile, "r") as logger_file:
            logger_list = json.load(logger_file)
        yield from client.send_message(message.channel, (logger_list))    
        print(logger_list)
    
        
client.run('MzY0MTQ1NTQxNTE4NzIxMDQ0.DLLgeQ.sv36d_sD-2ePU7j89GSeeigeKQc')