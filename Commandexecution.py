from MessageManager import MessageManager
from Cooldown import Cooldown
from SongManager import SongList,\
    TurnSongOffAndReturnMessage, TurnSongOnAndReturnMessage, RunSongOn,\
    TurnRandomSongOffAndReturnMessage, RunRandomSongOn, RemoveSong,\
    TurnRandomSongOnAndReturnMessage, SihaInformation, Listcheck,\
    StorePlayedSongs, RouletteOff, RouletteOn, RouletteRun, Current
    
class Commandexecute():
    
    commands = []
    fileName = 'Just dance unlimited.txt'   
    songListObj = SongList(fileName)
    line = "test"
    siha = SihaInformation()
    msgManager = MessageManager(line)
    cooldown = Cooldown()
    
    def __init__(self):
        self.tbot = "twerkrobot"
        self.tbot2 = "twerkbot"
        self.dancing = "dance"
        self.commandName = "No Command"
    
    def createCommands(self):
        
        self.commands.append(TurnSongOffAndReturnMessage(self.songListObj))
        self.commands.append(TurnSongOnAndReturnMessage(self.songListObj))
        self.commands.append(RunSongOn(self.songListObj))
        self.commands.append(TurnRandomSongOnAndReturnMessage(self.songListObj))
        self.commands.append(TurnRandomSongOffAndReturnMessage(self.songListObj))
        self.commands.append(RunRandomSongOn(self.songListObj))
        self.commands.append(RemoveSong(self.songListObj))
        self.commands.append(Twerk())
        self.commands.append(Trigger())
        self.commands.append(ModCommand())
        self.commands.append(Listcheck(self.songListObj))
        self.commands.append(StorePlayedSongs(self.songListObj))
        self.commands.append(RouletteOn(self.songListObj))
        self.commands.append(RouletteRun(self.songListObj))
        self.commands.append(RouletteOff(self.songListObj))
        self.commands.append(Current(self.songListObj))
    
    def getMod(self):
        return self.siha.getMod()
       
    def getCommands(self):
        return self.commands
      
    def isAMatch(self,msgManager):
        if self.commandName in msgManager.getMessage():
            return True
            
    def Run(self,msgManager):
        print("do nothing")
        
    def getReturnMsg(self,msgManager):
        return("")

class Twerk(Commandexecute):
    
    def __init__(self):
        self.commandName = "twerk"
    
    def getReturnMsg(self,msgManager):
        if self.cooldown.processCommandThreeMin(Twerk):
            return ("/me sihaButt I shall shake my posterior for you human *twerkles* sihaButt")
    
class Trigger(Commandexecute):
    
    def __init__(self):
        self.commandName = ["wtf is this", "dance pls", "make it jingle"]
        self.triggerListExecute = [
        "This is what we would like to call dancing, " 
        + "it's really fun sihaGood",
        "Please do not tell her to dance, "
        + "she will dance when she is ready sihaShark sihaAAA",
        "Avery doesn't feel comfortable twerking on stream. Sorry! However, "
        + "I am a bot, so I can make twerk for you. sihaShark"]
        
    def isAMatch(self,msgManager):
        for x in self.commandName:
            if x in msgManager.getMessage():
                return True
                #break
    
     
    def getReturnMsg(self,msgManager):
        for command,trigger in zip(self.commandName,self.triggerListExecute):
            if command in msgManager.getMessage() and self.cooldown.processCommandFive(command):
                return ("@" + msgManager.getUser() + " " +  trigger)
            #break
    

        
class ModCommand(Commandexecute):
    
    def __init__(self):
        self.commandName = ["!console","!whatistbot","!nospam","!name","!nobackseat"]
        self.modCommandExecute = ["/me If you have a big enough room, "
        + "Siha recommends using the Xbox with the Kinect sihaHype (but keep"
        + " in mind, the Kinect has been discontinued.) If you don't have a "
        + "lot of space, the Switch version is great and has bonus "
        + "choreographies sihaButt and features that other consoles don't have. sihaOmg",
        "/me Twerkrobot is a handmade bot coded in Python. Criogenesis, "
        + "one of our mods, made it! sihaHype",
        "/me Do not spam requests in chat, Avery will get to you when she can."
        + " If you spam requests we'll time you out as a warning and Ban if you continue",
        "/me Please don't call Avery creepy names of endearment or degrading"
        + " names. Calling her Littlesiha, Siha, or Avery is okay, but things "
        + "like 'sexy', 'wife', 'honey', 'babe', etc. will be given a warning "
        + "purge and timed out after if it continues",
        "/me Please do not backseat or provide solutions to puzzles unless "
        + "Avery specifically asks for help from the chat. You will be purged "
        + "as a warning and then timed out if you continue."]
        
    def isAMatch(self,msgManager):
        for x in self.commandName:
            if msgManager.getUser() in self.getMod() and x in msgManager.getMessage():
                return True
    
    def getReturnMsg(self,msgManager):
        for command,trigger in zip(self.commandName,self.modCommandExecute):
            #print(trigger)
            if command in msgManager.getMessage() and self.cooldown.processCommandFive(command):
                return (trigger)
                     
"""     


danceList = ["why aren't you dancing", "why arent you dancing", "why is she not dancing", "dance dance dance", "dance for me avery",
"keep dancing", "please dance now","dance bitch", "dance already", "get back to dancing", "this isnt dancing","I came here for dancing",
"why doesn't she dance", "why is she sitting down", "start dancing", "dance more", "I thought she danced", "show feet","feet please",
"show us your feet","when does she dance?","why no dance?", "is she dancing yet", "when will she dance", "when is she dancing", "why won't she dance"
"when does she dance again", "I want dancing", "dance dammit", "why isnt she dancing","go back to dancing"]

if message.strip() in danceList:
    sendMessage(s, "/timeout " + user + " 1")
    break
"""