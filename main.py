import time
import mysql.connector

global active #boolean that keeps program looping


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
def enterProgram(x):
    canEnter = False
    #ADMIN VERIFICATION
    if x == True:
        pass

    #makes sure id exists in data base
    search = 'SELECT ID FROM bank_accounts'
    cursor.execute(search)
    acctIDs = cursor.fetchall()

    print(acctIDs)
    
    accountNUM = int(input("Account Number: "))
    for x in acctIDs:
        ID = x[0]
        if ID == accountNUM:
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
        
    print("Sorry, that account is not in our system")
    return canEnter

#User has logged in with existing account , prints menu, called in main()
def existingUser():
    canEnter = enterProgram(False)
    if canEnter == True:
        printmenu()


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
    newACCTbalance = int(input("Account balance: "))
    query = "UPDATE bank_accounts SET balance = %s WHERE ID = %s"
    val = (newACCTbalance, newACCTID)
    cursor.execute(query, val)
    connection.commit()
    query = "SELECT * FROM bank_accounts WHERE ID = %s"
    val = (newACCTID, )
    cursor.execute(query, val)
    newACCTinfo = cursor.fetchone()
    print(newACCTinfo)


#User is a bank admin (NEED TO ADD TRUE OR FALSE ADMIN COLUMN TO MYSQL)
def bankAdmin():
    #can enter program will go through admin values
    canEnter = enterProgram(True)
    if canEnter == True:
        adminActive = True
        while adminActive:
            print('1. Create New Account\n2. Close Account\n3. Modify an Account')
            if userType == "1":
                newUser()
            elif userType == "2":
                pass
            elif userType == "3":
                pass
            else:
                print("Exiting...")
                adminActive = False
                break

    else:
        print("Sorry, you are not a bank administrator")

#Prints menu, called in existingUser()
def printmenu():
    print("//\n 1. Check Balance\n 2. Make Deposit\n 3. Make Withdrawl")
    #NEEDS FUNCTION TO DO EACH OF THESE !!!
    action = input("Enter action request: ")
    if action == "1": 
        #bankAdmin()
        pass
    elif action == "2":
        pass
        
    elif action == "3":
        pass
    else:
        print("Exiting...")
        active = False
        break


def main():
    #Keeps program running and cuts when false
    active = True

    print("Hello! Welcome to the online banking program!")
    
    while active:
        userType = selectUserType()
        if userType == "1": 
            #bankAdmin()
            pass
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
