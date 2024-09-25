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
tasks = [""]
###########################################login###
def login():
    loop1 = 3
    loop2 = 3
    username(loop1, loop2)

def username(loop1, loop2):
    usrname = ("jacob")
    usr = input("Enter Username: ")
    if usr == usrname:
        check = True
        password(loop2,check)
    else:
        counter1(loop1,loop2)
        
def password(loop2, check):
    passwrd = ("290408")
    pas = input("Enter Password: ")
    if pas == passwrd:
        check2 = True
        checks(check,check2)
    else:
        counter2(loop2,check)

def counter1(loop1,loop2):
    if loop1 == 0:
        lock()
    else:
        loop1 = loop1 - 1
        print("Invalid Username",loop1,"attempts left")
        username(loop1,loop2)

def counter2(loop2, check):
    if loop2 == 0:
        lock()
    else:
        loop2 = loop2 - 1
        print("Invalid Username",loop2,"attempts left")
        password(loop2,check)


def lock():
    print("Locked Out")

def checks(check, check2):
    if check == True:
        if check2 == True:
            print("You are now logged in")
    else:
        print("Error")
        
        
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
    loop = 0
    check = False
    for arg in argv:
        check = True
        if loop == 0:
            file = arg
    if check != True:
        file = input("Choose a name for your new file: ")
    filen = file+".txt"
    f = open(filen, "x")
    print("File created")
    f.close()
############################################################appendfile###
def appendfile(*argv):
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
    filen = file+".txt"
    phrase = phrase+". "
    f = open(filen, "a")
    f.write(phrase)
    print("Appended to file")
    f.close()
############################################################writefile###
def writefile(*argv):
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
    filen = file+".txt"
    f = open(filen, "w")
    f.write(phrase)
    print("Written to file")
    f.close()
############################################################deletefile###
def deletefile(*argv):
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
    filen = file+".txt"
    if ovr == "overide":
        import os
        os.remove(filen)
        print("Deleted",filen,)
    else:
        check = input("Are you sure you want to delete this file? Y/N: ")
        if check == "Yes" or check == "Y" or check == "y" or check == "yes":
            import os
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
    filen = file+".txt"    
    f = open(filen, "r")
    print(f.read())

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



if __name__ == "__main__":
    supercheck = True