###jacoobsmodules###
# https://github.com/vinta/awesome-python?tab=readme-ov-file
# jmod.login
# jmod.greet
# jmod.calc
# jmod.agecalc
# jmod.gettime
# jmod.getdate
# jmod.getday
# jmod.createfile
# jmod.appendfile
# jmod.writefile
# jmod.deletefile
# jmod.readfile
# jmod.dbsearch
# jmod.dbedit
# jmod.rps
# jmod.createtodolist
# jmod.addtask
# jmod.checkofftask
# jmod.deletetask
# jmod.opentodolist
# jmod.fileconvert
# jmod.translate
# jsacm.aid
# jsacm.ewans
# jsacm.profitcalc
# jsacm.caesarcypher
# jsacm.namegen
# jsacm.convert
# jsacm.rickroll
# jsacm.ytplay
# jsacm.ytdownload
tasks = [""]
features = ['aid = lists all features in this release','login = login system (requires {username,password}','calc = sophisticated calculator','agecalc = age calculator','gettime = prints the current time','getdate = prints the current date','getday = prints the current day','createfile = creates a new text file','appendfile = appends a text file','writefile = writes into a text file','deletefile = deletes a text file','readfile = reads a text file','dbsearch = searches an SQL databse','dbedit = edits an SQL database','rps = rock paper scissors','createtodolist = creates a todolist','addtask = add a task to a todolist','checkofftask = check task off todolist','deletetask = deletes a task of the todolist','opentodolist = reads the contents of the todolist','fileconvert = converts files to many different formats','translate = translates a phrase into any language','profitcalc = A simple profit calculator','caesarcypher = a simple cypher to make codes','namegen = generates a random full name','convert = a simple unit converter','ytplay = plays a youtube video of choice from a url','ytdownload = downloads a youtube video form a url']
###########################################help###
def aid():
    print("Avaliable features in this release are")
    for i in features:
        print(i)
###########################################login###
def login(username,password):
    usrname = username
    passwrd = password
    while True:
        usr = input("Enter username: ")
        if usr == usrname:
            break
        else:
            print("Incorrect username")
    while True:
        pas = input("Enter password: ")
        if pas == passwrd:
            print("You are now logged in")
            break
        else:
            print("Incorrect password")
        
        
################################################calc###        
        
import math
import sys
   
# String in the form above
# Using either, plus, add, minus, subtract, muplitply, times,  divide (operand is taken from first 2 letters)


#Converts the seperated 'int' characters that are as strings in elements into one string under operand
def calc_operand_collector(operand_list, numb_list):
    operand = "0"
    for n in range(operand_list.index(" ")):
        if operand_list[n] in numb_list:
            operand = operand + operand_list[n]
    return operand


#Turns word operators into integers
def calc_operator_collector(list):
    op = ""
    for n in range(len(list)):
        if list[n] == "p" and list[n + 1] == "l" or list[n] == "a" and list[n + 1] == "d":
            op = 0
        elif list[n] == "m" and list[n + 1] == "i" or list[n] == "s" and list[n + 1] == "u":
            op = 1
        elif list[n] == "m" and list[n + 1] == "u" or list[n] == "t" and list[n + 1] == "i":
            op = 2
        elif list[n] == "d" and list[n + 1] == "i":
            op = 3
    return op


#Main body subroutine
def calc(*argv):
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            string = arg
    if check != True:
        string = input("Enter your calculation: ")
    #Var & list declarations
    numb_list = ["0","1","2","3","4","5","6","7","8","9"]
    operand_list = []
    list = [*string]
    ans = 0


    #Finds what operation to do
    op = calc_operator_collector(list)


    #Creates a list of all the numbers in 'list' adding spaces to differentiate different operands    
    for n in range(len(list)):
        if list[n] in numb_list or list[n] == " ":
            operand_list.append(list[n])  
    operand_list.append(" ")
    #Makes the frst operand whole and integers again
    operand0 = int(calc_operand_collector(operand_list, numb_list))


    #Does stuff to make the next subroutine work
    for n in range(operand_list.index(" ") + 2):
        operand_list.pop(0)


    #Makes the second operand whole and integers again
    operand1 = int(calc_operand_collector(operand_list, numb_list))
   
    #Does the calculation
    if op == 0:
        ans = operand0 + operand1
    elif op == 1:
        ans = operand0 - operand1
    elif op == 2:
        ans = operand0 * operand1
    elif op == 3:
        ans = operand0 / operand1
    print(string,"is", ans)


  
############################################################greeting###
def greet(*argv):
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            name = arg
    if check != True:
        name = ""
    from datetime import datetime
    now = datetime.now()
    time = now.hour
    if time < 12:
        phr = "Good morning"
    elif time < 16:
        phr = "Good afternoon"
    elif time < 19:
        phr = "Good evening"
    else:
        phr = "Good night"
    print(phr,name)


############################################################time###
def gettime():
    import time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    
    
############################################################date###
def getdate():
    from datetime import date
    today = date.today()
    print("Today's date:", today)

############################################################createfile###
def createfile(*argv):
    import os
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            file = arg
    if check != True:
        file = input("Choose a name for your new file: ")
    filen = "Created Files/"+file+".txt"
    if os.path.isfile(filen) == True:
        print("File with that name allready exists")
    else:
        newpath = r'Created Files' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        f = open(filen, "x")
        print("File created")
        f.close()
############################################################appendfile###
def appendfile(*argv):
    import os
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            file = arg
            loop = loop+1
        if loop == 1:
            phrase = arg
    if check != True:
        file = input("enter file name: ")
        phrase = input("enter phrase to append into file: ")
    filen = "Created Files/"+file+".txt"
    if os.path.isfile(filen) == False:
        print("File with that name dosen't exist")
    else:
        phrase = phrase+". "
        f = open(filen, "a")
        f.write(phrase)
        print("Appended to file")
        f.close()
############################################################writefile###
def writefile(*argv):
    import os
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            file = arg
            loop = loop+1
        if loop == 1:
            phrase = arg
    if check != True:
        file = input("enter file name: ")
        phrase = input("enter phrase to write into file: ")
    phrase = phrase+". "
    filen = "Created Files/"+file+".txt"
    if os.path.isfile(filen) == False:
        print("File with that name dosen't exist")
    else:
        f = open(filen, "w")
        f.write(phrase)
        print("Written to file")
        f.close()
############################################################deletefile###
def deletefile(*argv):
    import os
    loop = 0
    check = False
    for arg in argv:
        check1 = True
        if loop == 0:
            file = arg
            loop = loop +1
        if loop == 1:
            ovr = arg
    if check1 != True:
        file = input("enter file name: ")
    filen = "Created Files/"+file+".txt"
    if os.path.isfile(filen) == False:
        print("File with that name dosen't exist")
    else:
        if ovr == "overide":
            import os
            os.remove(filen)
            print("Deleted",filen,)
        else:
            check = input("Are you sure you want to delete this file? Y/N: ")
            if check == "Yes" or check == "Y" or check == "y" or check == "yes":
                os.remove(filen)
                print("Deleted",filen,)
            else:
                print("Canceling")
############################################################readfile###
def readfile(*argv):
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            file = arg
    if check != True:
        file = input("enter file name: ")
    filen = "Created Files/"+file+".txt"
    if os.path.isfile(filen) == False:
        print("File with that name dosen't exist")
    else:
        f = open(filen, "r")
        print(f.read())
        f.close

############################################################databasesearch###
def dbsearch(*argv):
    import sqlite3
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            dbchoice = arg
            loop = loop+1
        if loop == 1:
            tblchoice = arg
            loop = loop+1
        if loop == 2:
            find = arg
    if check != True:
        dbchoice = input("Enter name of database to be searched: ")
        tblchoice = input("Enter table name: ")
        column = input("Enter column to search: ")
        find = input("Enter what you want to search for: ")
    DATABASE = dbchoice+".db"
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    sqlt = "SELECT *"
    sqlc = " FROM "+str(tblchoice)
    sqln = " WHERE "+str(column)+" = "+str(find) 
    sql = str(sqlt)+str(sqlc)+str(sqln)
    cur.execute(sql)
    print(cur.fetchall())

############################################################dbedit###
def dbedit(*argv):
    import sqlite3
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            dbchoice = arg
            loop = loop+1
        if loop == 1:
            choicetable = arg
            loop = loop+1
        if loop == 2:
            choicecolumn = arg
            loop = loop+1
        if loop == 3:
            choicevalue = arg
            loop = loop+1
        if loop == 4:
            newvalue = arg
    if check != True:
        dbchoice = input("Enter name of database to be searched: ")
        choicetable = input("Enter table name: ")
        choicecolumn = input("Enter column: ")
        choicevalue = input("Enter old/existing value: ")
        newvalue = input("Enter new value: ")
    DATABASE = dbchoice+".db"
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    sqlt = "UPDATE "+str(choicetable)
    sqlc = " SET "+str(choicecolumn)
    sqln = "WHERE "+str(choicecolumn)
    sql = str(sqlt)+str(sqlc)+' = ? '+sqln+' = ?'
    print(sql)
    cursor.execute(sql, (newvalue,choicevalue) )
    conn.commit()
############################################################Rockpaperscissors###
import random
    
def rps():
    print("sure lets see whos best")
    print("what have you chosen")
    usrchoice = input("...")
    print(usrchoice)
    choice = random.randint(1, 4)
    if choice == 1:
        print("I have chosen scissors")
        if usrchoice == "scissors":
            print("We have drawn")
        elif usrchoice == "rock":
            print("you won")
        elif usrchoice == "paper":
            print("you lost")
    elif choice == 2:
        print("I have chosen rock")
        if usrchoice == "rock":
            print("We have drawn")
        elif usrchoice == "paper":
            print("you won")
        elif usrchoice == "scissors":
            print("you lost")
    elif choice == 3:
        print("I have chosen paper")
        if usrchoice == "paper":
            print("We have drawn")
        elif usrchoice == "rock":
            print("you lost")
        elif usrchoice == "scissors":
            print("you won")

    else:
        print("error")


############################################################createtodolist###
def createtodolist():
    file = input("Choose name for your new todolist")
    filen = file+".txt"
    f = open(filen, "x")
    print("TODO list created")
    f.close()
    
############################################################opentotodolist###
def opentodolist():
    print("Tasks:")
    for index, task in enumerate(tasks):
        status = "Done" if task["done"] else ["Not Done"]
        print(f"{index + 1}. {task['task']} - {status}")

############################################################addtotodolist###
def addtask():
    print("Enter the new task")
    task = input("")
    tasks.append({"task": task, "done": False})
    print("Task added!")
    
############################################################checkofftodolist###
def checkofftask():
    task_index = int(input("Enter the task number to mark as done: ")) - 1
    if 0 <= task_index < len(tasks):
        tasks[task_index]["done"] = True
        print("Task marked as done!")
        
############################################################deletetodolist###
def deletetask():
    task_index = int(input("Enter the task number to be removed: ")) - 1
    if 0 <= task_index < len(tasks):
        tasks[task_index]["done"] = True
        print("Task Removed!")
        
############################################################age calculator###
def agecalc():
    from datetime import datetime, timedelta
    now = datetime.now()
    print("Enter your date of birth (YYYY-MM-DD):")
    dob_input = input()
    birthday = datetime.strptime(dob_input, "%Y-%m-%d")
    difference = now - birthday
    age_in_years = difference.days // 365
    print(f"You are {age_in_years} years old.")
    
############################################################get day###
def getday():
    import datetime
    now = datetime.datetime.now()
    print("Today is",now.strftime("%A"))

############################################################file type converter###
def fileconvert():
    import aspose.words as aw
    print("Avaliable formats to convert are DOC - DOC - RTF - DOT - DOTX - DOTM - DOCM - ODT - OTT - PDF - XPS - OpenXPS - PostScript - JPG - PNG - TIFF - BMP - SVG - EMF - GIF - HTML - MHTML - EPUB - MOBI - Xaml - PCL - etc")
    current = input("current file type: ")
    operator = input("File type to convert to")
    og = input("Enter name of file to convert: ")
    oldname = str(og)+"."+str(current)
    newname = str(og)+"."+str(operator)
    doc = aw.Document(oldname)
    doc.save(newname)
    

############################################################translate###
def translate(*argv):
    from deep_translator import GoogleTranslator
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            phrase = arg
            loop = loop+1
        if loop == 1:
            lang = arg
    if check != True:
        phrase = input("Enter phrase to translate: ")
        lang = input("choose the language to translate into: ")
    translated = GoogleTranslator(source='auto', target= lang).translate(str(phrase))  # output -> Weiter so, du bist großartig
    print(translated)
    

############################################################password generator###
def passgen(*argv):
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            N = arg
    import random
    import string
    if check != True:
        N = input("enter how long you would like the password to be: ")
    passwrd =''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation) for _ in range(int(N)))
    print(passwrd)

############################################################ewans module###
def ewans():
    print("Spam,Eggs and Ham")
    
    
############################################################profit calculator###
def profitcalc(*argv):
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            net_profit = arg
            loop = loop+1
        if loop == 1:
            costs = arg
    if check != True:
        net_profit = input("Enter the net profit: ")
        costs = input("Enter the total costs: ")
    print("The total profit is £"+str(int(net_profit)-int(costs)))
    
############################################################caesar cypher###
def caesarcypher(*argv):
    import random
    import string
    ans = []
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            usrinp = arg
    if check != True:
        usrinp = input("Enter phrase to input: ")
    n = random.randint(1,25)
    alphabet = string.ascii_lowercase
    for i in range(len(usrinp)):
        ch = usrinp[i]
        if ch==" ":
            ans.append(" ")
        elif (ch.isupper()):
            ans.append(str(chr((ord(ch) + n-65) % 26 + 65)))      
        else:
            ans.append(str(chr((ord(ch) + n-97) % 26 + 97)))
            an = ''.join(ans)
    print("Plain Text is : " + usrinp)
    print("Shift pattern is : " + str(n))
    print("Cipher Text is : " + str(an))

############################################################name generator###
def namegen():
    import names
    print(names.get_full_name())

############################################################unit converter###
def convert(*argv):
    factors = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.34,
        "milimeters": 0.001,
        "centimeters": 0.01,
        "meters": 1,
        "kilometers": 1000,
        "inches": 0.0254,
        "feet": 0.3048,
        "yard": 0.9144,
        "miles": 1609.34
    }
    convert = []
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            convert.append(arg)
            loop = loop+1
        if loop == 1:
            convert.append(arg)
            loop = loop+1
        if loop == 2:
            convert.append(arg)
    loop1 = 0
    for i in convert:
        loop1 = loop1+1
        if loop1 == 3:
            value = int(i)
        if loop1 == 4:
            from_unit = str(i)
        if loop1 == 5:
            to_unit = str(i)
    if check != True:
        value = float(input("Enter the value: "))
        from_unit = str(input("Enter the unit to convert from (e.g., km, mi, ft): "))
        to_unit = str(input("Enter the unit to convert to: "))
    meters = value * factors[from_unit]
    result = meters / factors[to_unit]
    print(f"{value} {from_unit} is equal to {result:.4f} {to_unit}")


############################################################rickroll###
def rickroll():
    from os import startfile
    startfile("nggup.mp4")
    
############################################################ytplay###
def ytplay(*argv):
    from pytube import YouTube
    import webbrowser
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            video_url = arg
    if check != True:
        video_url = input("Enter url of video you want to play")
    yt = YouTube(video_url)
    video_title = yt.title
    thumbnail_url = yt.thumbnail_url
    webbrowser.open(video_url)
    
############################################################ytdownload###
def ytdownload(*argv):
    import os
    from pytubefix import YouTube
    from pytubefix.cli import on_progress
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            url = str(arg)
    if check != True:
        url = input("Enter Url of video to download")
     
    yt = YouTube(url, on_progress_callback = on_progress)
    print(yt.title)
    newpath = r'YTDOWNLOADS' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    ys = yt.streams.get_highest_resolution()
    ys.download("YTDOWNLOADS/")

    
if __name__ == "__main__":
    supercheck = True
    
    
    
    
    
    
    
