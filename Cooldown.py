import time

class Cooldown():
    def __init__(self):
        self.test = "test"
        self.minCallFreq = 10
        self.threeMin = 180
        self.beginTime = 0
        self.used = {}
        
    def callCommand(self,command):
        print('Calling command `%s`.' % command)
    
    def cooldown(self,command):
        print('You have used command `%s` in the last %u seconds.' % (command, self.minCallFreq))
    
    def processCommandFive(self,command):
        if command not in self.used:
            print(command)
            self.used[command] = time.time() - self.minCallFreq
        
        if time.time() - self.used[command] < self.minCallFreq:
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
        