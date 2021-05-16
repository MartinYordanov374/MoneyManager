from tkinter import *
import json 
import mysql.connector
from dotenv import load_dotenv
import os
root=Tk()

root.title('MoneyManager')
root.geometry("800x600")

load_dotenv()
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=os.getenv('PASSWORD'),
  database="Mmanager"
)

class EmFund():
    def addMoneyEmFund():
        addScreen = Toplevel()
        addScreen.title('Deposit Money - Emergency Fund')
        addScreen.geometry("460x500")
        addMoneyPromptMessage = Label(addScreen,text='How much money would you like to deposit to your Emergency Fund?')
        addMoneyPromptMessage.grid(row=0, column=0)
        addMoneyField= Entry(addScreen)
        addMoneyField.grid(row=1, column=0, ipadx=130)
        finishAddingButton = Button(addScreen, text='Deposit money to your emergency fund',width=50, 
        command=lambda: EmFund.confirmAddingEmFundMoney(addMoneyField.get())).grid(row=2,column=0)
    
    def confirmAddingEmFundMoney(amount):
        if(len(amount)>0):
            currAmount = int(amount)
            formerAmount = int(emFundBox.get())
            emFundBox.delete(0,END)
            emFundBox.insert(0,currAmount+formerAmount)
            saveData()
            queryCursor = mydb.cursor()
            queryOne ='INSERT INTO TransactionHistory (type, amount) VALUES (%s, %s)'
            val=('deposit', amount)
            queryCursor.execute(queryOne,val)
            mydb.commit()

        else:
            errorScreen = Toplevel()
            errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
            errorMessage.pack()

    def withdrawMoneyEmFund():
        withdrawScreen = Toplevel()
        withdrawScreen.title('Withdraw Money - Emergency Fund')
        withdrawScreen.geometry('460x500')
        #ask message -> How muhc would you like to withdraw?
        withdrawPromptMessage = Label(withdrawScreen,text='How much money would you like to withdraw?')
        withdrawPromptMessage.grid(row=0, column=0)
        #input field
        withdrawInputField = Entry(withdrawScreen)
        withdrawInputField.grid(row=1, column =0, ipadx=130)
        #withdraw input button -> How much would you like to withdraw?
        withdrawButton = Button(withdrawScreen,text='Withdraw money from your emergency fund', width=50, 
        command=lambda: EmFund.confirmWithdrawEmFundMoney(withdrawInputField.get()))
        withdrawButton.grid(row=2, column=0)

    def confirmWithdrawEmFundMoney(amount):
            currentEmFundMoney = int(emFundBox.get())
            moneyToWithdraw = int(amount)
            if(len(amount)>=0 and moneyToWithdraw<=currentEmFundMoney):
                emFundBox.delete(0,END)
                emFundBox.insert(0,currentEmFundMoney-moneyToWithdraw)
                saveData()
                queryCursor = mydb.cursor()
                queryOne ='INSERT INTO TransactionHistory (type, amount) VALUES (%s, %s)'
                val=('withdraw', amount)
                queryCursor.execute(queryOne,val)
                mydb.commit()

            else:
                errorScreen = Toplevel()
                errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
                errorMessage.pack()

class MiscFund():
    def addMoneyMiscFund():
        addScreen = Toplevel()
        addScreen.title('Deposit Money - Miscellanious Fund')
        addScreen.geometry("475x500")
        addMoneyPromptMessage = Label(addScreen,text='How much money would you like to deposit to your Miscellanious Fund?')
        addMoneyPromptMessage.grid(row=0, column=0)
        addMoneyField= Entry(addScreen)
        addMoneyField.grid(row=1, column=0, ipadx=130)
        finishAddingButton = Button(addScreen, text='Deposit money to your Miscellanious fund',width=50, command=lambda: MiscFund.confirmAddingMiscFundMoney(addMoneyField.get())).grid(row=2,column=0)
    
    def confirmAddingMiscFundMoney(amount):
        if(len(amount)>0):
            currAmount = int(amount)
            formerAmount = int(thingsInputBox.get())
            thingsInputBox.delete(0,END)
            thingsInputBox.insert(0,currAmount+formerAmount)
            saveData()
            queryCursor = mydb.cursor()
            queryOne ='INSERT INTO TransactionHistory (type, amount) VALUES (%s, %s)'
            val=('deposit', amount)
            queryCursor.execute(queryOne,val)
            mydb.commit()

        else:
            errorScreen = Toplevel()
            errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
            errorMessage.pack()

    def withdrawMoneyMiscFund():
        withdrawScreen = Toplevel()
        withdrawScreen.title('Withdraw Money - Miscellanious Fund')
        withdrawScreen.geometry('475x500')
        #ask message -> How muhc would you like to withdraw?
        withdrawPromptMessage = Label(withdrawScreen,text='How much money would you like to withdraw?')
        withdrawPromptMessage.grid(row=0, column=0)
        #input field
        withdrawInputField = Entry(withdrawScreen)
        withdrawInputField.grid(row=1, column =0, ipadx=130)
        #withdraw input button -> How much would you like to withdraw?
        withdrawButton = Button(withdrawScreen,text='Withdraw money from your Miscellanious fund', width=50, command=lambda:MiscFund.confirmWithdrawMiscFundMoney(withdrawInputField.get()))
        withdrawButton.grid(row=2, column=0)

    def confirmWithdrawMiscFundMoney(amount):
        currentThingsFundMoney = int(thingsInputBox.get())
        moneyToWithdraw = int(amount)
        if(len(amount)>=0 and moneyToWithdraw<=currentThingsFundMoney):
            thingsInputBox.delete(0,END)
            thingsInputBox.insert(0,currentThingsFundMoney-moneyToWithdraw)
            saveData()
            queryCursor = mydb.cursor()
            queryOne ='INSERT INTO TransactionHistory (type, amount) VALUES (%s, %s)'
            val=('withdraw', amount)
            queryCursor.execute(queryOne,val)
            mydb.commit()

        else:
            errorScreen = Toplevel()
            errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
            errorMessage.pack()


emergencyFundLabel = Label(root, text='Emergency Fund:').grid(row=0, column=0)

#TEXTBOX - EMERGENCY FUND

#save data to the JSON file 
def saveData():
    data={
     'EmFund': emFundBox.get(),
     'MiscFund': thingsInputBox.get()
    }
    data_file = open('fundsData.json','w')
    json.dump(data, data_file, indent=6)

#read data from the JSON file 
def readData():
    savedMoney=[]
    data_file=open('fundsData.json')
    loaded_data = json.load(data_file)
    pairs = loaded_data.items()
    for key,value in pairs:
        savedMoney.append(value)
    global savedEmFundMoney, savedMiscMoney
    savedEmFundMoney = savedMoney[0]
    savedMiscMoney = savedMoney[1]


def readTransactionHistory():
    transactionHistoryScreen = Toplevel()
    transactionHistoryScreen.geometry('460x550')
    transactionHistoryTextBox = Listbox(transactionHistoryScreen, width=100, height=100)
    transactionHistoryTextBox.pack()
    
    queryCursor = mydb.cursor()
    sqlCommand ='SELECT type,amount FROM TransactionHistory'
    queryCursor.execute(sqlCommand)
    result = queryCursor.fetchall()
    mydb.commit()
    for i in result:
        transactionHistoryTextBox.insert(END,"--", i)
    # historyData_file = open('historyData.json')
    # loadedHistoryData = json.load(historyData_file)
    # historyDataPairs = loadedHistoryData.items()
    # global historyActionType, historyAmount
    # for key, value in historyDataPairs:
    #     historyActionType=key
    #     historyAmount=value

    
    # transactionHistoryTextBox.insert(0,historyActionType)

readData()

emFundBox = Entry(root, state='normal')
emFundBox.grid(row=0, column=1)
emFundBox.insert(0,savedEmFundMoney)

#WITHDRAW FROM EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW

emFundWithdrawButton = Button(root, text='Withdraw money', command=EmFund.withdrawMoneyEmFund).grid(row=1, column=0)

#ADD TO EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD

emFundAddButton = Button(root, text='Deposit money', command=EmFund.addMoneyEmFund).grid(row=1, column=1)

#BUTTON LABEL - THINGS
thingsLabel = Label(root, text='Miscellanious Fund: ')
thingsLabel.grid(row=2, column=0)
#TEXTBOX - THINGS FUND
thingsInputBox = Entry(root)
thingsInputBox.grid(row=2, column=1)
thingsInputBox.insert(0,savedMiscMoney)
#WITHDRAW FROM THINGS FUNDS -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW
withdrawThingsButton = Button(root, text='Withdraw Money', command=MiscFund.withdrawMoneyMiscFund)
withdrawThingsButton.grid(row=3, column=0)

#ADD TO THINGS FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD
depositThingsButton = Button(root, text='Deposit Money', command=MiscFund.addMoneyMiscFund)

depositThingsButton.grid(row=3, column=1)


#CREATE NEW FUND BUTTON
#DELETE FUND BUTTON

#SHOW HISTORY OF WITHDRAWALS AND DEPOSITS 
showHistoryButton = Button(root, text='show withdraw/deposit history', command=readTransactionHistory)
emptyLabel = Label(root, text='     ').grid(row=2, column=3)

showHistoryButton.grid(row=2, column=4)



root.mainloop()