import time
import mysql.connector

connection = mysql.connector.connect(user = 'root', database='lesson_3', password = 'R05esbe11@')
#cursor is table
cursor = connection.cursor()
testQuery = ("SELECT * FROM bank_accounts")
cursor.execute(testQuery)#sort all things in cursor

#goes through table
for item in cursor:
    print(item)

cursor.close()
connection.close()

#Accounts added to dictionary, each item contains a unique value/"pin"/"balance"
accountDict = {
    "1234" : {
        "pin" : "5678",
        "balance" : 0
    }
}

#User selects what action they would like to do, called in main()
def selectUserType():
    user = input("//\n 1. Bank Administrator Login\n 2. Existing User Login\n 3. New User \n 4. Quit\n//\n Enter Account Type: ")
    return user

#User logging in with existing account, returns TRUE if logged in, called in existingUser()
def enterProgram():
    canEnter = False
    search = 'SELECT ID FROM bank_accounts'
    cursor.execute(search)
    acctNUMS = cursor.fetchall()

    print(acctNUMS)
    
    accountNUM = int(input("Account Number: "))
    for x in accNUMS:
        if accountNUM == x:
            tempNUM = str(accountNUM)
            search = 'SELECT PIN FROM bank_accounts WHERE ID =' + tempNUM
            cursor.execute(search)
            acctPIN = cursor.fetchone()
            PIN = input("PIN: ")
            if PIN == acctPIN:
                canEnter = True
                return canEnter
            else:
                print("Incorrect PIN number, try again.")
    
    print("Sorry, that account is not in our system")
    return canEnter

#User has logged in with existing account , prints menu, called in main()
def existingUser():
    canEnter = enterProgram()
    if canEnter == True:
        printmenu()

#User would like to create an account, adds item to accountDict, called in main()   
def newUser():
    newACCTnum = input("New Account Number: ")
    if newACCTnum in accountDict:
        print("This account number already exists, try using another")
        newACCTnum = input("New Account Number: ")
    newACCTpin = input("New PIN: ")
    accountDict[newACCTnum] = {"pin" : newACCTpin, "balance" : 0}
    newACCTbalance = int(input("Account balance: "))
    accountDict[newACCTnum]["balance"] = newACCTbalance
    print(accountDict)


#Prints menu, called in existingUser()
def printmenu():
    print("//\n 1. Check Balance\n 2. Make Deposit\n 3. Make Withdrawl")
    #NEEDS FUNCTION TO DO EACH OF THESE !!!


def main():
    #Keeps program running and cuts when false
    active = True

    print("Hello! Welcome to the online banking program!")
    while active:
        userType = selectUserType()
        if userType == "1":
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
