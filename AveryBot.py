import time
from SocketControl import SocketControl
from MessageManager import MessageManager
from SongManager import SihaInformation,SongList
from Commandexecution import Commandexecute
from Cooldown import Cooldown



def main():
    siha = SihaInformation()
    manager = SocketControl()
    cmd = Commandexecute()
    
    cooldown = Cooldown()
    
    manager.prepareSocket(siha.CHANNEL)
    twitchSocket = manager.theSocket
    fileName = 'Just dance unlimited.txt'
    timestart = time.time()
    songListObj = SongList(fileName)
    songListObj.createSongList()
    #justDanceCommand = SongCommand(songList)
    bufferSize = 1024
    
    
    
    cmd.createCommands()
      
    while True:
        try:
            readBuffer = twitchSocket.recv(bufferSize)
            readBuffer = readBuffer.decode()
            temp = readBuffer.split("\n")
            readBuffer = readBuffer.encode()
            readBuffer = temp.pop()
        except:
            temp = ""
            
        for line in temp:
            #print(line)
            if line == "":
                break
            # So twitch doesn't timeout the bot.
            if "PING" in line and manager.Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                twitchSocket.send(msgg)
                #print(msgg)
                break
            # get user
            
        
            msgManager = MessageManager(line)
            # get message send by user'
            message = msgManager.getMessage()
            print(message)
            #cooldown.Timetest(timestart)
            commands = cmd.getCommands()
            #print(commands)
            for item in commands:
                match = item.isAMatch(msgManager)
                if (match == True):
                    item.Run(msgManager)
                    mes = item.getReturnMsg(msgManager)
                    manager.sendMessage(mes, siha.CHANNEL)
            
            
            
            # for you to see the chat from CMD
            #print(user + " > " + message)
            # sends private msg to the user (start line)
            #PMSG = "/w " + user + " "



if __name__ == '__main__':
    main()