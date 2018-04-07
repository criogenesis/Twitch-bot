### The only import you need!
import socket
import time
import random
### Cooldown variables
min_call_freq = 10
threemin = 180
begintime = 0
used = {}
jdnamelst = list()
jdsongdict = {}
count = 0
acceptingrequest = None
acceptingrandom = None
randomdict = {}
### Options (Don't edit)
SERVER = "irc.twitch.tv"  # server
PORT = 6667  # port
### Options (Edit this)
PASS = "oauth:rsxogjf9zuvtqm6q5o7ujxowesw4cn"  # bot password can be found on https://twitchapps.com/tmi/
BOT = "twerkrobot"  # Bot's name [NO CAPITALS]
CHANNEL = "criogenesis"  # Channal name [NO CAPITALS]
OWNER = "criogenesis"  # Owner's name [NO CAPITALS]
MOD = ['criogenesis', 'kompakt', 'dustyn', 'brosephstalin', 'littlesiha', 'unicorn_pudding', 'sammyy']
# moderator names [NO CAPITALS]


################################# Request Features ##################################
############ Here is where code goes when concerning song requests ############
############################################################################
import re
justdancelst = list()
jdlstcomplete = list()
justdanceun = 'Just dance unlimited.txt'
jh = open(justdanceun, encoding="ascii", errors="surrogateescape")
for line in jh:
    obj = "\'\'\[\[(.*?)\]\]\'\'"
    obj2 = "\[\'(.*?)\'\]"
    parsedata = re.findall(obj, line)
    if len(parsedata) < 1:
        continue
    else:
        justdancelst.append(parsedata)
     
justdancelststr = str(justdancelst)[1:-1]
#print(justdancelststr)
parsestr = re.findall(obj2, justdancelststr)
parsestrlower = [i.lower() for i in parsestr]
def remove_duplicateslow(parsestrlower):
    output = []
    seen = set()
    for value in parsestrlower:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output
def remove_duplicates(parsestr):
    output = []
    seen = set()
    for value in parsestr:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output
parseuniquelower = remove_duplicateslow(parsestrlower)
parseunique = remove_duplicateslow(parsestr)    

### Functions
 
def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    print(messageTemp)
    s.send((messageTemp + "\r\n").encode())
 
def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user
def getMessage(line):
    global message
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    message = message.encode('ascii', 'ignore') 
    message = message.decode()
    if '\'' in message:
        message = message.replace('\'',"")
    return message.lower()
def joinchat():
    readbuffer_join = "".encode()
    Loading = True
    while Loading:
        readbuffer_join = s.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        temp = readbuffer_join.split("\n")
        readbuffer_join = readbuffer_join.encode()
        readbuffer_join = temp.pop()
        for line in temp:
            Loading = loadingCompleted(line)
    #sendMessage(s, "Chat room joined!")
    print("Bot has joined " + CHANNEL + " Channel!")
 
def loadingCompleted(line):
    if ("End of /NAMES list" in line):
        return False
    else:
        return True
    
def call_command(command):
    print('Calling command `%s`.' % command)

def cooldown(command):
    print('You have used command `%s` in the last %u seconds.' % (command, min_call_freq))

def process_commandfive(command):
    if command not in used:
        used[command] = time.time() - min_call_freq
    
    if time.time() - used[command] < min_call_freq:
        return False 
    else:
        used[command] = time.time()
        return True
def process_command3min(command):
    if command not in used:
        used[command] = time.time() - threemin
    
    if time.time() - used[command] < threemin:
        return False 
    else:
        used[command] = time.time()
        return True
def jdusercheck(user):
    if user not in jdnamelst:
        jdnamelst.append(user)
        print('test 1')
        return True
    else:
        #print('test 22')
        return False
        
def jdsongcheck(i): 
    global count
    if i not in jdsongdict:
        jdsongdict[i] = 1
        print('song initialized')
    else:
        jdsongdict[i] += 1
    print('song added')
    print(jdsongdict)
def randomcheck(x):
    global count
    if x not in randomdict:
        randomdict[x] = 1
        print(randomdict)
    else:
        randomdict[x] += 1
        print('vote counted')
        print(randomdict)
        
    ### Code runs
s_prep = socket.socket()
s_prep.connect((SERVER, PORT))
s_prep.send(("PASS " + PASS + "\r\n").encode())
s_prep.send(("NICK " + BOT + "\r\n").encode())
s_prep.send(("JOIN #" + CHANNEL + "\r\n").encode())
s = s_prep
joinchat()
readbuffer = ""
 
def Console(line):
    # gets if it is a user or twitch server
    if "PRIVMSG" in line:
        return False
    else:
        return True
 
 
while True:
        try:
            readbuffer = s.recv(1024)
            readbuffer = readbuffer.decode()
            temp = readbuffer.split("\n")
            readbuffer = readbuffer.encode()
            readbuffer = temp.pop()
        except:
            temp = ""
        for line in temp:
            if line == "":
                break
            # So twitch doesn't timeout the bot.
            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                s.send(msgg)
                #print(msgg)
                break
            # get user
            user = getUser(line)
            # get message send by user'
            #lineE = line.encode('utf-8')
            
            message = getMessage(line)
            print(message)
            #print(type(message))
            #print(locale.getpreferredencoding())
            # for you to see the chat from CMD
            #print(user + " > " + message)
            # sends private msg to the user (start line)
            PMSG = "/w " + user + " "
            




################################# Command ##################################
############ Here you can add as meny commands as you wish of ! ############
############################################################################
            
            
            clubquestion = "club"
            tbot = "twerkrobot"
            tbot2 = "twerkbot"
            dancing = "dance"
            twerkrequest = "twerk"
            boyfriend = "does she have a boyfriend"
            bf =  "does she have a bf"
            sr = "!sr"
            requeston = "!requeston"
            requestoff = "!requestoff"
            case = "!case"
            songclear = "!songclear"
            randomsongon = "!randomsongon"
            randomsongoff = "!randomsongoff"
            vote = "!vote"
            one = "1"
            two = "2"
            slur1 = "nigg"
            slur2 = "nibba"
            unlimitedlstlower = [s.replace("\\udc92", "") for s in parseuniquelower]
            unlimitedlst = [s.replace("\\udc92", "") for s in parseunique] 
            print(unlimitedlstlower)
            print(unlimitedlst)
            songchoice1 = random.choice(unlimitedlst)
            songchoice2 = random.choice(unlimitedlst)
            
            
            
            commandlist = ["/me If you're asking if Avery goes to clubs, the answer is no sihaShark","/me sihaButt I shall shake my posterior for you human *twerkles* sihaButt","/me Yes, Avery has a boyfriend and his name is Sam, his channel is twitch.tv/iamsp00n sihaShark","/me Nancy Drew, you're off the case!",
            "/me The Just Dance Unlimited request feature has now been started! copy and paste your desired just dance unlimited song (exactly from the wiki). Requests are read as follows: !sr songname. A vote will be counted to see the top requested song. LITERALLY NO 2018 SONGS WILL WORK LIKE NONE OF THEM LITERALLY ZERO 2018 SONGS.",
            "/me @littlesiha The results have been tallied, the winner of the song request is: ",
            "Stop triggering this command you fuck",("/me The random request feature is now live, if you would like to see Avery dance to either" 
            + " (" + songchoice1 + ") " + "or" + " (" + songchoice2 + ") " + "type !vote 1 for" + " (" + songchoice1 + "), " + "or type !vote 2 for"+ " (" + songchoice2 + ") " + 
            "in chat")]
            
            for triggerlst, triggerlstre in zip(["wtf is this","dance pls","make it jingle","who is sam"],
            ["This is what we would like to call dancing, it's really fun sihaGood","Please do not tell her to dance, she will dance when she is ready sihaShark sihaREE",
            "Avery doesn't feel comfortable twerking on stream. Sorry! However, I am a bot, so I can make twerk for you. sihaShark","Sam is her boyfriend sihaShark"]):
                if triggerlst in message and process_commandfive(triggerlst):
                    sendMessage(s, "@" + user + " " + triggerlstre)
                    break
            
            for executelst, executelstre in zip(["!console","!whatistbot","!nospam","!name","!nobackseat"],
            ["/me If you have a big enough room, Siha recommends using the Xbox with the Kinect sihaHype (but keep in mind, the Kinect has been discontinued.) If you don't have a lot of space, the Switch version is great and has bonus choreographies sihaButt and features that other consoles don't have. sihaOmg",
            "Twerkrobot is a handmade bot coded in Python. Criogenesis, one of our mods, made it! sihaHype",
            "/me Do not spam requests in chat, Avery will get to you when she can. If you spam requests we'll time you out as a warning and Ban if you continue",
            "/me Please don't call Avery creepy names of endearment or degrading names. Calling her Littlesiha, Siha, or Avery is okay, but things like 'sexy', 'wife', 'honey', 'babe', etc. will be given a warning purge and timed out after if it continues",
            "/me Please do not backseat or provide solutions to puzzles unless Avery specifically asks for help from the chat. You will be purged as a warning and then timed out if you continue."]):
                if user in MOD and executelst in message and process_commandfive(executelst):
                    sendMessage(s, executelstre)
                    break
            
            dancelist = ["why aren't you dancing", "why arent you dancing", "why is she not dancing", "dance dance dance", "dance for me avery",
            "keep dancing", "please dance now","dance bitch", "dance already", "get back to dancing", "this isnt dancing","I came here for dancing",
            "why doesn't she dance", "why is she sitting down", "start dancing", "dance more", "I thought she danced", "show feet","feet please",
            "show us your feet","when does she dance?","why no dance?", "is she dancing yet", "when will she dance", "when is she dancing", "why won't she dance"
            "when does she dance again", "I want dancing", "dance dammit", "why isnt she dancing","go back to dancing"]
            
            if message.strip() in dancelist:
                sendMessage(s, "/timeout " + user + " 1")
                break
            if user == "dustyn" and "wtf is this" in message and process_commandfive("wtf is this"):
                sendMessage(s, "@" + user + " " + commandlist[6])
                break
            if slur1 in message or slur2 in message:
                sendMessage(s, "/timeout " + user)
                break
            if clubquestion in message and dancing in message and process_commandfive(clubquestion):
                sendMessage(s, commandlist[0])
                break
            if twerkrequest in message and not tbot in message and not tbot2 in message and process_command3min(twerkrequest):
                sendMessage(s, commandlist[1])
                break
            if boyfriend in message or bf in message and process_command3min(boyfriend):
                sendMessage(s, commandlist[2])
                break
            if user in MOD and songclear in message and process_commandfive(requestoff):
                jdsongdict.clear()
                print('Its off, list cleared')
                print(jdsongdict)
                break
            if user in MOD and requeston in message and process_commandfive(requeston):
                acceptingrequest = True
                sendMessage(s, commandlist[4])
                print('feature is on')
            if user in MOD and randomsongon in message and process_commandfive(randomsongon):
                acceptingrandom = True
                sendMessage(s, commandlist[7])
                randomlstdict = {songchoice1:"1",songchoice2:"2"} 
                print(randomlstdict)
                print(randomdict)
                #sendMessage(s, songchoice1 + " " + "," +  songchoice2)
            if "list check" in message:
                print('They already requested a song')
                print(jdnamelst)
                print(jdsongdict)
                #print(randomlst)
                print(randomdict)
                break
            
               
        while True:
            if acceptingrandom == True:
                for x,y in randomlstdict.items():
                    if y in message and vote in message and jdusercheck(user):
                        randomcheck(x)
                        print('in it')
                        break
                #break
            try:
                if user in MOD and randomsongoff in message and process_commandfive(randomsongoff):
                    acceptingrandom = False
                    winningrandom = max(randomdict, key=randomdict.get)
                    randomdict.clear()
                    del jdnamelst[:]
                    #del randomlst[:]
                    sendMessage(s, commandlist[5] + winningrandom)
                    print('Its off, list cleared')
                    print(randomdict)
                    print(randomlstdict)
                    #print('aaaaaaaaah')
                    break
                else:
                    #print('blahblah')
                    break
            except:
                #print('going here')
                break
    
        while True:
            if acceptingrequest == True:
                #print('test')
                if user in MOD and "!remove" in message:
                    for i in unlimitedlstlower:
                        if i in jdsongdict and i in message:
                            print("boop")
                            del jdsongdict[i]
                            sendMessage(s, i + " was removed from the song list")
                
                for i in unlimitedlstlower:
                    if i in message and sr in message and jdusercheck(user):
                        jdsongcheck(i)
                        print('in it')
                        break
                    
            try: 
                if user in MOD and requestoff in message and process_commandfive(requestoff):
                    winningsong = max(jdsongdict, key=jdsongdict.get)
                    acceptingrequest = False
                    del jdnamelst[:]
                    jdsongdict.clear()
                    sendMessage(s, commandlist[5] + winningsong)
                    print('Its off, list cleared')
                    print(jdnamelst)
                    print(jdsongdict)
                    break
                else:
                    #print('leaving loop')
                    break
            except:
                break
            
                
        #while True:
            #if user in MOD and case in message and process_commandfive(case):
                #count = count + 1
                #counts = str(count)
                #sendMessage(s, commandlist[3] + " Number of times off the case: " + counts)
            #break

                    