import time
import mysql.connector

global active #boolean that keeps program looping
global adminActive #keeps admin looping

connection = mysql.connector.connect(user = 'root', database='lesson_3', password = 'R05esbe11@')
#cursor is table
cursor = connection.cursor()
testQuery = ("SELECT * FROM bank_accounts")
cursor.execute(testQuery)#sort all things in cursor

#goes through table
for item in cursor:
    print(item)



#User selects what action they would like to do, called in main()
def selectUserType():
    user = input("//\n 1. Bank Administrator Login\n 2. Existing User Login\n 3. New User \n 4. Quit\n//\n Enter Account Type: ")
    return user

#User logging in with existing account, returns TRUE if logged in, called in existingUser()
def enterProgram(admin):
    canEnter = False
    #ADMIN VERIFICATION
    if admin == True:
        #Gets ID and checks if admin is actually true in acct
        search = 'SELECT ID FROM bank_accounts'
        cursor.execute(search)
        acctIDs = cursor.fetchall()

        #print(acctIDs)
        
        accountNUM = int(input("Account Number: "))
        for x in acctIDs:
            ID = x[0]
            if ID == accountNUM:
                validID = True
                break
            else:
                validID = False

        #If admin value does NOT equal zero this function proceeds, if it equals zero exits
        sql = "SELECT admin FROM bank_accounts WHERE ID = %s"
        val = (accountNUM, )
        cursor.execute(sql, val)
        adminResult = cursor.fetchone()
        isAdmin =adminResult[0]

        #if this acct id has a true admin value then proceed
        if isAdmin:
            pass
        
        #else if this acct id admin value = 0 then return false
        else: 
            print("Sorry, you are not a bank administrator")
            return False

    #makes sure id exists in data base
    else:
        search = 'SELECT ID FROM bank_accounts'
        cursor.execute(search)
        acctIDs = cursor.fetchall()

        print(acctIDs)
        
        accountNUM = int(input("Account Number: "))
        for x in acctIDs:
            ID = x[0]
            if ID == accountNUM:
                global THEONEANDONLYID 
                THEONEANDONLYID = ID
                validID = True
                break
            else:
                validID = False

    if validID == True:
        search = 'SELECT PIN FROM bank_accounts WHERE ID = %s'
        vals = (accountNUM, )
        cursor.execute(search, vals)
        countresult = cursor.fetchone()
        thePIN =countresult[0]

        PIN = int(input("PIN: "))
        if PIN == thePIN:
            canEnter = True
            return canEnter
        else:
            print("Incorrect PIN number, try again.")
    else:
        print("Sorry, that account is not in our system")

    return canEnter

#User has logged in with existing account , prints menu, called in main()
def existingUser():
    canEnter = enterProgram(False)
    if canEnter == True:
        printmenu(THEONEANDONLYID)


#User would like to create an account, adds item to accountDict, called in main()
#Needs to add a true/false bank admin value to row and to mysql
def newUser():
    #newACCTnum = input("Making new account?(y/n) ")
    testQuery = "SELECT MAX(ID) FROM bank_accounts "
    #lastID = countresult[0][0]
    cursor.execute(testQuery)
    countresult = cursor.fetchone()
    lastID =countresult[0]
#assigns the next available id number to this new user
    newID = int(lastID) + 1
    print("Your ID is now: " + str(newID))
    newACCTID = str(newID)
    newACCTpin = input("New PIN: ")
    addACCTQuery = "INSERT INTO bank_accounts(PIN, balance) VALUES (%s, %s);"
    val = (newACCTpin, 0)
    cursor.execute(addACCTQuery, val)
    connection.commit()
    newACCTbalance = float(input("Account balance: "))
    query = "UPDATE bank_accounts SET balance = %s WHERE ID = %s"
    val = (newACCTbalance, newACCTID)
    cursor.execute(query, val)
    connection.commit()
    newACCTadmin = bool(input("Are you an admin(true/false): "))
    query = "UPDATE bank_accounts SET admin = %s WHERE ID = %s"
    val = (newACCTadmin, newACCTID)
    cursor.execute(query, val)
    connection.commit()
    query = "SELECT * FROM bank_accounts WHERE ID = %s"
    val = (newACCTID, )
    cursor.execute(query, val)
    newACCTinfo = cursor.fetchone()
    print(newACCTinfo)


#Admin inputs 1,2,3 then inputs acctnum if statements for balance, pin, admin modification  called in adminAction()
def modifyAccount():
    modifyAction = input('Enter action request: ')
    inputID = int(input("ID: "))
    if modifyAction == "1": #modify balance
        num = input("(2)Deposit or (3)Withdrawl: ")
        editBalance(num, inputID)
    elif modifyAction == "2": #modify pin
        newPIN = input('New PIN: ')
        sql = "UPDATE bank_accounts SET pin = %s WHERE ID = %s"
        val = (newPIN, inputID)
        cursor.execute(sql, val)
        connection.commit()
    elif modifyAction == "3": #modify admin status
        isAdmin = input("Admin Status (true or false): ")
        if isAdmin == "true":
            isAdmin = int("1")
        elif isAdmin == "false":
            isAdmin = int("0")
        sql = "UPDATE bank_accounts SET admin = %s WHERE ID = %s"
        val = (isAdmin, inputID)
        cursor.execute(sql, val)
        connection.commit()


#Admin can create account, close account, modify account // called in bankAdmin() and calls newUser()
def adminAction(userInput):
    if userInput == "1": #Create account
        newUser()
    elif userInput == "2": #Close account
        inputID = int(input("ID: "))
        sql = "DELETE FROM bank_accounts WHERE ID = %s"
        val = (inputID, )
        cursor.execute(sql, val)
        connection.commit()
        print("Account number " + str(inputID) + " sucessfully deleted")
    elif userInput == "3": #Modify account
        print("1) Modify Balance \n2) Modify Pin \n3) Modify Admin Status\n")
        modifyAccount()
    else:
        print("Exiting...")
        return False
    return True

#User is a bank admin
def bankAdmin():
    #can enter program will go through admin values
    canEnter = enterProgram(True)
    if canEnter == True:
        adminActive = True
        while adminActive:
            print('1. Create New Account\n2. Close Account\n3. Modify an Account')
            action = input("Enter action request: ")
            adminActive = adminAction(action)
        

#function to edit bank account balance called in printmenu()
def editBalance(action, ID):
    if action == "1": #Check balance
        sql = 'SELECT balance FROM bank_accounts WHERE ID = %s'
        val = (ID, )
        cursor.execute(sql, val)
        balanceResult = cursor.fetchone()
        balance = str(balanceResult[0])
        print('You have $' + balance + ' in your account')
    elif action == "2": #Make deposit
        #gets balance
        sql = 'SELECT balance FROM bank_accounts WHERE ID = %s'
        val = (ID, )
        cursor.execute(sql, val)
        balanceResult = cursor.fetchone()
        balance = float(balanceResult[0])
        #gets deposit amount
        depositAmount = float(input('Deposit amount: '))
        newBalance = depositAmount + balance
        sql = "UPDATE bank_accounts SET balance = %s WHERE ID = %s"
        val = (newBalance, ID)
        cursor.execute(sql, val)
        connection.commit()
    elif action == "3": #Make withdrawl
        #gets balance
        sql = 'SELECT balance FROM bank_accounts WHERE ID = %s'
        val = (ID, )
        cursor.execute(sql, val)
        balanceResult = cursor.fetchone()
        balance = float(balanceResult[0])
        #gets withdrawl amount
        withdrawlAmount = float(input('Withdrawl amount: '))
        newBalance = balance - withdrawlAmount
        sql = "UPDATE bank_accounts SET balance = %s WHERE ID = %s"
        val = (newBalance, ID)
        cursor.execute(sql, val)
        connection.commit()
    else:
        print("Exiting...")
        return False
    return True

#Prints menu, called in existingUser()
def printmenu(ID):
    global userActive
    userActive = True
    while userActive:
        print("//\n 1. Check Balance\n 2. Make Deposit\n 3. Make Withdrawl")
        #NEEDS FUNCTION TO DO EACH OF THESE !!!
        action = input("Enter action request: ")
        userActive = editBalance(action, ID)

    

    


def main():
    #Keeps program running and cuts when false
    active = True

    print("Hello! Welcome to the online banking program!")
    
    while active:
        userType = selectUserType()
        if userType == "1": 
            bankAdmin()
            
        elif userType == "2":
            existingUser()
            
        elif userType == "3":
            newUser()
        else:
            print("Exiting...")
            active = False
            break
        #Makes easier on the eyes
        time.sleep(1)
        print("Going back home...")
        time.sleep(2)
        print()
        print()
    

main()
cursor.close()
connection.close()
