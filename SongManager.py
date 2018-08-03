import re
import random
from Cooldown import Cooldown

class SihaInformation():
    
    def __init__(self):
        self.CHANNEL = "criogenesis"  # Channal name [NO CAPITALS]
        self.MOD = [
        'criogenesis', 
        'kompakt', 
        'dustyn', 
        'brosephstalin', 
        'littlesiha', 
        'unicorn_pudding', 
        'sammyy', 
        'godfiend',
        'unsanewolf'
        ]
        
    def getChannel(self):
        return self.CHANNEL
    
    def getMod(self):
        return self.MOD
    

class SongList():
 
    randomSongChoices = {}   
    def __init__(self, fileName):
        self.songList = list()
        self.firstBracketFind= "\'\'\[\[(.*?)\]\]\'\'"
        self.secondBracketFind = "\[\'(.*?)\'\]"
        self.fileName = fileName
        self.createSongList()
        self.firstSongChoice = random.choice(self.songList)
        self.secondSongChoice = random.choice(self.songList)
        self.settupRandomSongs()
        
        
        
    def removeSongDuplicates(self):
        output = []
        seen = set()
        for value in self.songList:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output
    
    def makeSongListLowercase(self):
        self.songList = [x.lower() for x in self.songList]    
    
    def createSongList(self):
        fh = open(self.fileName, encoding="ascii", errors="surrogateescape")
        for line in fh:
            extractSong = re.findall(self.firstBracketFind, line)
            if len(extractSong) < 1:
                continue
            else:
                self.songList.append(extractSong)
        songListToString = str(self.songList)[1:-1]
        self.songList = re.findall(self.secondBracketFind, songListToString)    
        self.removeSongDuplicates()
        self.songList = [s.replace("\\udc92", "") for s in self.songList]
    
    def settupRandomSongs(self):
        firstSongChoice = random.choice(self.songList)
        secondSongChoice = random.choice(self.songList)
        self.randomSongChoices = {firstSongChoice:"1",secondSongChoice:"2"}
        #print(self.randomSongChoices)  
          
    def getSongList(self):
        return self.songList
               
class SongCommand():
    requestSongFlag = None   
    randomSongFlag = None
    usernameList = list()
    songChoiceAndCount = {}
    randomSongChoiceAndCount = {}               
    def __init__(self, songListObj):
        
        self.siha = SihaInformation()
        self.commandName = "No Command"
        self.songListObj = songListObj
        self.cooldown = Cooldown()
        
        
    def getMod(self):
        return self.siha.getMod()
        
    def isAMatch(self,msgManager):
        if msgManager.getUser() in self.getMod() and self.commandName in msgManager.getMessage():
            return True
            
    def Run(self,msgManager):
        print("do nothing")
        
    def getReturnMsg(self,msgManager):
        return("")
        
    def checkUsername(self,msgManager):
        if msgManager.getUser() not in self.usernameList:
            self.usernameList.append(msgManager.getUser())
            print('test 1')
            return True
        else:
            #print('test 22')
            return False
    
    def updateSongCountForUser(self,song):
        if song not in SongCommand.songChoiceAndCount:
            
            SongCommand.songChoiceAndCount[song] = 1
            print('song initialized')
        else:
            
            SongCommand.songChoiceAndCount[song] += 1
        print('song added')
        print(SongCommand.songChoiceAndCount)
        
    def updateRandomSongCountForUser(self,song):
        if song not in self.randomSongChoiceAndCount:
            self.randomSongChoiceAndCount[song] = 1
            print(self.randomSongChoiceAndCount)
        else:
            print(self.randomSongChoiceAndCount)
            self.randomSongChoiceAndCount[song] += 1
            print('vote counted')
            print(self.randomSongChoiceAndCount)
           

                        
class TurnRandomSongOffAndReturnMessage(SongCommand):
    
    def __init__(self, songListObj):
        super(TurnRandomSongOffAndReturnMessage, self).__init__(songListObj)
        self.commandName = "!randomsongoff"
        self.winningRandomSong = None
        
    def Run(self,msgManager):
        try:
            SongCommand.randomSongFlag = False
            self.winningRandomSong = max(self.randomSongChoiceAndCount, key=self.randomSongChoiceAndCount.get)
            del self.usernameList[:]
            self.randomSongChoiceAndCount.clear()
            print('Its off, list cleared')
            print(self.randomSongChoiceAndCount)
            
        except:
            self.winningRandomSong = None
            print("went here because of crash")
            pass
        
    def getReturnMsg(self,msgManager):
        if self.winningRandomSong == None:
            return None
        return("/me @littlesiha The results have been tallied, the winner of the song request is: " + self.winningRandomSong)
                    
class TurnRandomSongOnAndReturnMessage(SongCommand):
    
    def __init__(self, songListObj):
        super(TurnRandomSongOnAndReturnMessage, self).__init__(songListObj)
        self.commandName = "!randomsongon"
        
        #songListObj.settupRandomSongs()
        self.randomSongChoices = songListObj.randomSongChoices
        self.firstSongChoice = list(self.randomSongChoices)[0]
        self.secondSongChoice = list(self.randomSongChoices)[1]
        
        
    def Run(self,msgManager):
        SongCommand.randomSongFlag = True
        print('feature is on')
        
    def getReturnMsg(self,msgManager):
        if self.cooldown.processCommandFive(TurnRandomSongOnAndReturnMessage): 
            return ("/me The random request feature is now live, if you would "
            + "like to see Avery dance to either (" + self.firstSongChoice 
            + ") " + "or" + " (" + self.secondSongChoice + ") " + "type !vote "
            + "1 for" + " (" + self.firstSongChoice + "), or type !vote 2 for" 
            + " (" + self.secondSongChoice + ") in chat")
        return None
                
class RunRandomSongOn(SongCommand):
    
    def __init__(self,songListObj):
        super(RunRandomSongOn, self).__init__(songListObj)
        self.commandName = "!vote"
        self.runningObj = TurnRandomSongOnAndReturnMessage(songListObj)
        
    def isAMatch(self,msgManager):
        if self.commandName in msgManager.getMessage():
            return True    
        
    def Run(self,msgManager): 
        if SongCommand.randomSongFlag == True:
            #print(self.runningObj.randomSongChoices)
            for x,y in self.runningObj.randomSongChoices.items():
                if y in msgManager.getMessage() and self.checkUsername(msgManager):
                    self.updateRandomSongCountForUser(x)
                    print('in it')
                    
class TurnSongOffAndReturnMessage(SongCommand):
    
    def __init__(self,songListObj):
        super(TurnSongOffAndReturnMessage, self).__init__(songListObj)
        self.commandName = "!requestoff"
        self.winningSong = None
        
    def Run(self,msgManager):
            
        try:
            SongCommand.requestSongFlag = False
            #$print(SongCommand.requestSongFlag)
            self.winningSong = max(SongCommand.songChoiceAndCount, key=SongCommand.songChoiceAndCount.get)
            del self.usernameList[:]
            SongCommand.songChoiceAndCount.clear()
            print('Its off, list cleared')
            print(self.usernameList)
            print(SongCommand.songChoiceAndCount)
            
        except:
            print("went here because of crash")
            self.winningSong = None
            pass
        
    def getReturnMsg(self,msgManager):
        if self.winningSong == None:
            return None
        return("/me @littlesiha The results have been tallied, the winner of the song request is: " + self.winningSong) 
        
        
class RemoveSong(SongCommand):
    
    def __init__(self, songListObj):
        super(RemoveSong, self).__init__(songListObj)
        self.commandName = "!remove"
        
    def getReturnMsg(self, msgManager):
        if SongCommand.requestSongFlag == True:
            print('test')
            songList = self.songListObj.getSongList()
            for i in songList:
                if i in SongCommand.songChoiceAndCount and i in msgManager.getMessage():
                    print("boop")
                    del SongCommand.songChoiceAndCount[i]
                    return (i + " was removed from the song list")
                                    
class RunSongOn(SongCommand):
    
    def __init__(self, songListObj):
        super(RunSongOn, self).__init__(songListObj)
        self.commandName = "!sr"
        self.songListObj.makeSongListLowercase()

    def isAMatch(self,msgManager):
        if self.commandName in msgManager.getMessage():
            return True
            
    def Run(self,msgManager):
        print(SongCommand.requestSongFlag)
        songList = self.songListObj.getSongList()
        
        if SongCommand.requestSongFlag == True:
            for i in songList:
                if i in msgManager.getMessage() and self.checkUsername(msgManager):
                    print("yeet2")
                    self.updateSongCountForUser(i)
                    print('in it')
                    break
                                  
class TurnSongOnAndReturnMessage(SongCommand):
    
    def __init__(self, songListObj):
        super(TurnSongOnAndReturnMessage, self).__init__(songListObj)
        self.commandName = "!requeston" 
       
    
    def Run(self,msgManager):
        SongCommand.requestSongFlag = True
        print('feature is on')
        
    def getReturnMsg(self,msgManager):
        if self.cooldown.processCommandFive(TurnSongOnAndReturnMessage):
            return (
            "/me The Just Dance Unlimited request feature has now been "
            + "started! copy and paste your desired just dance unlimited song "
            "(exactly from the wiki). Requests are read as follows: !sr "
            + "songname. A vote will be counted to see the top requested song."
            + " LITERALLY NO 2018 SONGS WILL WORK LIKE NONE OF THEM LITERALLY "
            +"ZERO 2018 SONGS."
            )
        return None
    
class Listcheck(SongCommand):
    
    def __init__(self,songListObj):
        super(Listcheck, self).__init__(songListObj)
        self.commandName = "!listcheck"
        
    def Run(self, msgManager):
        print('They already requested a song')
        print(self.usernameList)
        print(SongCommand.songChoiceAndCount)
        #print(randomlst)
        print(self.randomSongChoiceAndCount)      
        


                           


                    

    
    
        
        

                
    
            

            
            