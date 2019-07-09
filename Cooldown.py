import time


class Cooldown():
    def __init__(self):
        self.test = "test"
        self.minCallFreq = 10
        self.songRepost = 60
        self.threeMin = 180
        self.beginTime = 0
        self.used = {}
        self.beginTime = time.time()
        
    def callCommand(self,command):
        print('Calling command `%s`.' % command)
    
    def cooldown(self,command):
        print('You have used command `%s` in the last %u seconds.' % (command, self.minCallFreq))
    
    def processCommandFive(self,command):
        if command not in self.used:
            #print(self.used)
            self.used[command] = time.time() - self.minCallFreq
        
        if time.time() - self.used[command] < self.minCallFreq:
            #print(self.used)
            return False
            
        else:
            self.used[command] = time.time()
            return True
    def processCommandThreeMin(self,command):
        if command not in self.used:
            self.used[command] = time.time() - self.threeMin
        
        if time.time() - self.used[command] < self.threeMin:
            return False 
        else:
            self.used[command] = time.time()
            return True
    
    def processCommand60(self,command,flag):
        if flag != True:
            #print("one")
            self.used[command] = time.time()
            #print(self.used)
            return False
        if command not in self.used:
            self.used[command] = time.time() - self.songRepost
        
        if time.time() - self.used[command] < self.songRepost:
            #print("two",time.time() - self.used[command])
            #self.used[command] = time.time()
            return False
    
        if time.time() - self.used[command] == 60:
            #print("three",time.time() - self.used[command])
            self.used[command] = time.time()
            return False
        
        else:
            #print("four",time.time() - self.used[command])
            self.used[command] = time.time()
            return True
        
        
        
        
        
        
        
        
        
        
        