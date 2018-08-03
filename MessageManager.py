


class MessageManager():
    
    def __init__ (self,line):
        self.line = line
        
        
    def getUser(self):
        separate = self.line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user
    
    def getMessage(self):
        global message
        try:
            message = (self.line.split(":", 2))[2]
        except:
            message = ""
        message = message.encode('ascii', 'ignore') 
        message = message.decode()
        if '\'' in message:
            message = message.replace('\'',"")
        return message.lower()
    
    
        