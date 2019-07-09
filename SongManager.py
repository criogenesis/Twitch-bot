import time
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
    
    def makeSongListLowercase(self, songList):
        songList = [x.lower() for x in songList]
        return songList    
    
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
        songLen = len(self.songList)
        playedLen = len(SongCommand.playedSongs)
        
        while(firstSongChoice == secondSongChoice or
              (firstSongChoice in SongCommand.playedSongs or 
               secondSongChoice in SongCommand.playedSongs)):
            secondSongChoice = random.choice(self.songList)
            if(songLen-1 <= playedLen):
                firstSongChoice = "ITS FULL"
                secondSongChoice = "STILL FULL"
            if(firstSongChoice in SongCommand.playedSongs):
                firstSongChoice = random.choice(self.songList)
        self.randomSongChoices = {firstSongChoice:"1",secondSongChoice:"2"}
          
    def getSongList(self):
        return self.songList
               
class SongCommand():
    requestSongFlag = False   
    randomSongFlag = False
    rouletteSongFlag = False
    usernameList = list()
    songChoiceAndCount = {}
    randomSongChoiceAndCount = {}
    timeStart = time.time()
    playedSongs = set()
    rouletteSongs = set()
                  
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
        return 5
        
    def getReturnMsg(self,msgManager):
        return("")
        
    def checkUsername(self,msgManager):
        if msgManager.getUser() not in self.usernameList:
            self.usernameList.append(msgManager.getUser())
            return True
        else:
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
            self.playedSongs.add(self.winningRandomSong.lower())
            del self.usernameList[:]
            self.randomSongChoiceAndCount.clear()
            self.songListObj.randomSongChoices.clear()
            print('Its off, list cleared')
            print(self.randomSongChoiceAndCount)
            print(self.songListObj.randomSongChoices)
            
        except:
            SongCommand.randomSongFlag = False
            self.winningRandomSong = None
            print("went here because of crash")
            pass
        
    def getReturnMsg(self,msgManager):
        if self.winningRandomSong == None:
            return None
        return(
        "/me @littlesiha The results have been tallied, the winner of "
        +"the song request is: " + self.winningRandomSong
        )
                    
class TurnRandomSongOnAndReturnMessage(SongCommand):
    
    def __init__(self, songListObj):
        super(TurnRandomSongOnAndReturnMessage, self).__init__(songListObj)
        self.commandName = "!randomsongon"
        self.firstSongChoice = ""
        self.secondSongChoice = ""
        self.sendmsg = False
        
        
    def Run(self,msgManager):
        if (SongCommand.requestSongFlag == False 
            and SongCommand.rouletteSongFlag == False
            and SongCommand.randomSongFlag == False):
            SongCommand.randomSongFlag = True
            self.sendmsg = True
            self.songListObj.settupRandomSongs()
            self.firstSongChoice = list(self.songListObj.randomSongChoices)[0]
            self.secondSongChoice = list(self.songListObj.randomSongChoices)[1]
        
    def getReturnMsg(self,msgManager):
        if self.cooldown.processCommandFive(TurnRandomSongOnAndReturnMessage) and self.sendmsg: 
            self.sendmsg = False
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
        
    def isAMatch(self,msgManager):
        if self.commandName in msgManager.getMessage():
            return True    
        
    def Run(self,msgManager):
        
        if SongCommand.randomSongFlag == True:
            for x,y in self.songListObj.randomSongChoices.items():
                if y in msgManager.getMessage() and self.checkUsername(msgManager):
                    self.updateRandomSongCountForUser(x)
                    print('in it')

class Current(SongCommand):
    
    def __init__(self,songListObj):
        super(Current, self).__init__(songListObj)
        self.commandName = "!current"    
    
    def getReturnMsg(self,msgManager):
        if (SongCommand.randomSongFlag == True):
            return (
            "/me The current feature is Random Song. Vote 1 for "
            + list(self.songListObj.randomSongChoices)[0]
            + " or Vote 2 for "
            + list(self.songListObj.randomSongChoices)[1]
            )
        if (SongCommand.requestSongFlag == True):
            return (
            "/me The current feature is Request Song."
            )
        if (SongCommand.rouletteSongFlag == True):
            return (
            "/me The current feature is Roulette."
            )
        else:
            return (
                "/me No vote currently running."
                )
        return None   
    
    
class TurnSongOffAndReturnMessage(SongCommand):
    
    def __init__(self,songListObj):
        super(TurnSongOffAndReturnMessage, self).__init__(songListObj)
        self.commandName = "!requestoff"
        self.winningSong = None
        
    def Run(self,msgManager):
            
        try:
            SongCommand.requestSongFlag = False
            del self.usernameList[:]
            print(self.usernameList)
            self.winningSong = max(SongCommand.songChoiceAndCount, key=SongCommand.songChoiceAndCount.get)
            self.playedSongs.add(self.winningSong.lower())
            SongCommand.songChoiceAndCount.clear()
            print('Its off, list cleared')
            print(SongCommand.songChoiceAndCount)
            
        except:
            SongCommand.requestSongFlag = False
            print("went here because of crash")
            self.winningSong = None
            pass
        
    def getReturnMsg(self,msgManager):
        if self.winningSong == None:
            return None
        return(
        "/me @littlesiha The results have been tallied, the winner of "
        + "the song request is: " + self.winningSong
        ) 
        
        
class RemoveSong(SongCommand):
    
    def __init__(self, songListObj):
        super(RemoveSong, self).__init__(songListObj)
        self.commandName = "!remove"
        
    def getReturnMsg(self, msgManager):
        if SongCommand.requestSongFlag == True or SongCommand.rouletteSongFlag == True:
            songList = self.songListObj.getSongList()
            for i in songList:
                #try:
                    if (i in SongCommand.songChoiceAndCount and i in msgManager.getMessage()):
                        del SongCommand.songChoiceAndCount[i]
                        return (i + " was removed from the song list")
                #except:
                    if (i in self.rouletteSongs and i in msgManager.getMessage()):
                        SongCommand.rouletteSongs.remove(i)
                        return (i + " was removed from the song list")
    
                                    
class RunSongOn(SongCommand):
    
    def __init__(self, songListObj):
        super(RunSongOn, self).__init__(songListObj)
        self.commandName = "!sr"
        
    def isAMatch(self,msgManager):
        if self.commandName in msgManager.getMessage():
            return True
            
    def Run(self,msgManager):
        songList = self.songListObj.getSongList()
        songListOrig = self.songListObj.getSongList()
        songList = SongList.makeSongListLowercase(self, songList)
        
        if SongCommand.requestSongFlag == True:
            for i in songList:
                if (i in msgManager.getMessage() and i not in self.playedSongs 
                and self.checkUsername(msgManager)):
                    for x in songListOrig:
                        if x.lower() == i:
                            self.updateSongCountForUser(x)
                            break
                    print(self.playedSongs)
                    print('in it')
                    break
                
    def getReturnMsg(self,msgManager):
        try:
            theSongSpace = msgManager.getMessage().split("\r", 1)[0]
            theSong = theSongSpace.split(" ", 1)[1]
        except:
            theSong = ""
        #print(theSong)'
        if (self.cooldown.processCommand60(RunSongOn,SongCommand.requestSongFlag)
            and SongCommand.requestSongFlag == True):
            return (
            "/me MrDestructoid BEEP, REPOST "
            + "Song Voting is on! Just Dance Unlimited songs only (!jdu). Use '!sr songname'. "
            + "Songs from JD2019 will not work. Only your first vote counts."
            )
        if (SongCommand.requestSongFlag == True and theSong in self.playedSongs):
            return(
            "@" 
            + msgManager.getUser() 
            + " sorry, Avery has already "
            + "danced to that today! Feel free to request another song!"
            )
                                  
class TurnSongOnAndReturnMessage(SongCommand):
    
    
    def __init__(self, songListObj):
        super(TurnSongOnAndReturnMessage, self).__init__(songListObj)
        self.commandName = "!requeston"
        self.sendmsg = False
       
    
    def Run(self,msgManager):
        if (SongCommand.requestSongFlag == False 
            and SongCommand.rouletteSongFlag == False
            and SongCommand.randomSongFlag == False):
            SongCommand.requestSongFlag = True
            self.sendmsg = True
    
    def getReturnMsg(self,msgManager):
        print(self.sendmsg)
        if (self.cooldown.processCommandFive(TurnSongOnAndReturnMessage) and self.sendmsg):
            self.sendmsg = False
            return (
            "/me Song Voting is on! Just Dance Unlimited songs only (!jdu). Use !sr songname. "
            + "Songs from JD2019 will not work. Only your first vote counts."
            )
        return None
    
class StorePlayedSongs(SongCommand):
    
    def __init__(self,songListObj):
        super(StorePlayedSongs, self).__init__(songListObj)
        self.commandName = "!played"
        
    def getReturnMsg(self, msgManager):
        songList = self.songListObj.getSongList()
        songListOrig = self.songListObj.getSongList()
        songList = SongList.makeSongListLowercase(self, songList)
        for i in songList:
            if i in msgManager.getMessage() and i not in self.playedSongs:
                for x in songListOrig:
                    if x.lower() == i:
                        self.playedSongs.add(i)
                print(self.playedSongs)
                return ("/me " + i + " was added to the list of songs already played!")
            
            

class RouletteOn(SongCommand):
    
    def __init__(self,songListObj):
        super(RouletteOn, self).__init__(songListObj)
        self.commandName = "!rouletteon"
        self.sendmsg = False
    
    def Run(self,msgManager):
        if (SongCommand.requestSongFlag == False 
            and SongCommand.rouletteSongFlag == False
            and SongCommand.randomSongFlag == False):
            SongCommand.rouletteSongFlag = True
            self.sendmsg = True
    
    def getReturnMsg(self,msgManager):
        if self.cooldown.processCommandFive(TurnSongOnAndReturnMessage) and self.sendmsg:
            self.sendmsg = False
            return (
            "/me Roulette voting is on! If you request a song, it may get randomly selected. " 
            + "Just Dance Unlimited songs only (type !jdu to view the Unlimited song list.) "
            + "Use '!sr songname' to request a song. "
            + "Songs from JD2019 will not work. Only your first vote counts."
            )
            
        return None
    
class RouletteRun(SongCommand):
    def __init__(self,songListObj):
        super(RouletteRun, self).__init__(songListObj)
        self.commandName = "!sr"
    
    def isAMatch(self,msgManager):
        if self.commandName in msgManager.getMessage():
            return True
        
    def Run(self,msgManager):
        songList = self.songListObj.getSongList()
        songListOrig = self.songListObj.getSongList()
        songList = SongList.makeSongListLowercase(self, songList)
        
        if SongCommand.rouletteSongFlag == True:
            for i in songList:
                if (i in msgManager.getMessage() and i not in self.playedSongs
                    and self.checkUsername(msgManager)):
                    for x in songListOrig:
                        if x.lower() == i:
                            self.rouletteSongs.add(x)
                    print(self.playedSongs)
                    print(self.rouletteSongs)
                    print('in it')
                    break
                
    def getReturnMsg(self,msgManager):
        try:
            theSongSpace = msgManager.getMessage().split("\r", 1)[0]
            theSong = theSongSpace.split(" ", 1)[1]
        except:
            theSong = ""
        if (self.cooldown.processCommand60(RouletteRun,SongCommand.
            rouletteSongFlag) and SongCommand.rouletteSongFlag == True):
            return (
            "/me MrDestructoid BEEP, REPOST "
            + "Roulette voting is on! If you request a song, it may get randomly selected. " 
            + "Just Dance Unlimited songs only (type !jdu to view the Unlimited song list.) "
            + "Use '!sr songname' to request a song. "
            + "Songs from JD2019 will not work. Only your first vote counts."
            )
        if (SongCommand.rouletteSongFlag == True and theSong in self.playedSongs):
            return(
            "@" 
            + msgManager.getUser() 
            + " sorry, Avery has already "
            + "danced to that today! Feel free to request another song!"
            )

class RouletteOff(SongCommand):
    
    def __init__(self,songListObj):
        super(RouletteOff, self).__init__(songListObj)
        self.commandName = "!rouletteoff"
        self.winningRoulette = ""
        
    def Run(self,msgManager):
        try:
            SongCommand.rouletteSongFlag = False
            self.winningRoulette = random.choice(list(self.rouletteSongs))
            self.playedSongs.add(self.winningRoulette.lower())
        except:
            self.winningRoulette = ""
            SongCommand.rouletteSongFlag = False
            print("went here because of crash")
            pass
        
    def getReturnMsg(self,msgManager):
        if self.winningRoulette == "":
            del self.usernameList[:]
            return None
        del self.usernameList[:]
        self.rouletteSongs.clear()
        print('Its off, list cleared')
        print(self.usernameList)
        print(self.rouletteSongs)
        return(
        "/me @littlesiha The results have been tallied, the winner of "
        + "the roulette is: " + self.winningRoulette
        ) 
    
                
class Listcheck(SongCommand):
    
    def __init__(self,songListObj):
        super(Listcheck, self).__init__(songListObj)
        self.commandName = "!listcheck"
        
    def Run(self, msgManager):
        print('They already requested a song')
        print(self.usernameList)
        print(SongCommand.songChoiceAndCount)
        print(self.randomSongChoiceAndCount)      
        


                           


                    

    
    
        
        

                
    
            

            
            