import socket


class SocketControl():
    ### Options (Don't edit)
    def __init__(self):
        self.SERVER = "irc.twitch.tv"  # server
        self.PORT = 6667  # port
        ### Options (Edit this)
        self.PASS = "oauth:rsxogjf9zuvtqm6q5o7ujxowesw4cn"  # bot password can be found on https://twitchapps.com/tmi/
        self.BOT = "twerkrobot"  # Bot's name [NO CAPITALS]
        self.OWNER = "criogenesis"  # Owner's name [NO CAPITALS]
        self.theSocket = socket.socket()
    
    def prepareSocket(self,CHANNEL):
        self.theSocket.connect((self.SERVER, self.PORT))
        self.theSocket.send(("PASS " + self.PASS + "\r\n").encode())
        self.theSocket.send(("NICK " + self.BOT + "\r\n").encode())
        self.theSocket.send(("JOIN #" + CHANNEL + "\r\n").encode())
        self.joinChat(CHANNEL)
        #readBuffer = ""
        
    def sendMessage(self,message,CHANNEL):
        try:
            messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
            print(messageTemp)
            self.theSocket.send((messageTemp + "\r\n").encode())
        except:
            pass
    
    
    def joinChat(self,CHANNEL):
        readBuffer_join = "".encode()
        Loading = True
        bufferSize = 1024
        while Loading:
            readBuffer_join = self.theSocket.recv(bufferSize)
            readBuffer_join = readBuffer_join.decode()
            temp = readBuffer_join.split("\n")
            readBuffer_join = readBuffer_join.encode()
            readBuffer_join = temp.pop()
            for line in temp:
                Loading = self.loadingCompleted(line)
        #sendMessage(s, "Chat room joined!")
        print("Bot has joined " + CHANNEL + " Channel!")
     
    def loadingCompleted(self,line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True
        
    def Console(self,line):
        # gets if it is a user or twitch server
        if "PRIVMSG" in line:
            return False
        else:
            return True
