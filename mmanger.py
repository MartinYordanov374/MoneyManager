from tkinter import *
import json
from dotenv.main import find_dotenv 
import mysql.connector
from dotenv import load_dotenv
import os

#Creating the window
root=Tk()

root.title('MoneyManager')
root.geometry("850x600")

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
            formerAmount = int(GUI.emFundBox.get())
            GUI.emFundBox.delete(0,END)
            GUI.emFundBox.insert(0,currAmount+formerAmount)
            DataOperations.saveData()
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
            currentEmFundMoney = int(GUI.emFundBox.get())
            moneyToWithdraw = int(amount)
            if(len(amount)>=0 and moneyToWithdraw<=currentEmFundMoney):
                GUI.emFundBox.delete(0,END)
                GUI.emFundBox.insert(0,currentEmFundMoney-moneyToWithdraw)
                DataOperations.saveData()
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
            formerAmount = int(GUI.thingsInputBox.get())
            GUI.thingsInputBox.delete(0,END)
            GUI.thingsInputBox.insert(0,currAmount+formerAmount)
            DataOperations.saveData()
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
        currentThingsFundMoney = int(GUI.thingsInputBox.get())
        moneyToWithdraw = int(amount)
        if(len(amount)>=0 and moneyToWithdraw<=currentThingsFundMoney):
            GUI.thingsInputBox.delete(0,END)
            GUI.thingsInputBox.insert(0,currentThingsFundMoney-moneyToWithdraw)
            DataOperations.saveData()
            queryCursor = mydb.cursor()
            queryOne ='INSERT INTO TransactionHistory (type, amount) VALUES (%s, %s)'
            val=('withdraw', amount)
            queryCursor.execute(queryOne,val)
            mydb.commit()

        else:
            errorScreen = Toplevel()
            errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
            errorMessage.pack()

class DataOperations():
    def saveData():
        data={
        'EmFund': GUI.emFundBox.get(),
        'MiscFund': GUI.thingsInputBox.get()
        }
        data_file = open('fundsData.json','w')
        json.dump(data, data_file, indent=6)
    
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

DataOperations.readData()

class GUI():
    def emFundGUI():
        GUI.emergencyFundLabel = Label(root, text='Emergency Fund:').grid(row=0, column=0)

        #TEXTBOX - EMERGENCY FUND
        GUI.emFundBox = Entry(root, state='normal')
        GUI.emFundBox.grid(row=0, column=1)
        GUI.emFundBox.insert(0,savedEmFundMoney)

        #WITHDRAW FROM EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW

        GUI.emFundWithdrawButton = Button(root, text='Withdraw money', command=EmFund.withdrawMoneyEmFund).grid(row=1, column=0)

        #ADD TO EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD

        GUI.emFundAddButton = Button(root, text='Deposit money', command=EmFund.addMoneyEmFund).grid(row=1, column=1)

    def thingsFundGUI():
        #BUTTON LABEL - THINGS
        GUI.thingsLabel = Label(root, text='Miscellanious Fund: ')
        GUI.thingsLabel.grid(row=2, column=0)
        #TEXTBOX - THINGS FUND
        GUI.thingsInputBox = Entry(root)
        GUI.thingsInputBox.grid(row=2, column=1)
        GUI.thingsInputBox.insert(0,savedMiscMoney)
        #WITHDRAW FROM THINGS FUNDS -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW
        GUI.withdrawThingsButton = Button(root, text='Withdraw Money', command=MiscFund.withdrawMoneyMiscFund)
        GUI.withdrawThingsButton.grid(row=3, column=0)

        #ADD TO THINGS FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD
        GUI.depositThingsButton = Button(root, text='Deposit Money', command=MiscFund.addMoneyMiscFund)

        GUI.depositThingsButton.grid(row=3, column=1)

    def optionsGUI():
        global rowCounter, colCounter
        rowCounter = 5
        colCounter = 0
        #SHOW HISTORY OF WITHDRAWALS AND DEPOSITS 
        showHistoryButton = Button(root, text='show withdraw/deposit history', command=DataOperations.readTransactionHistory)
        emptyLabel = Label(root, text='     ').grid(row=2, column=3)

        showHistoryButton.grid(row=2, column=4)

        fundsAttributes=[]

        def createFundWindow():
            
            createFundWindow = Toplevel()
            createFundWindow.geometry('400x500')

            createFundNameLabel = Label(createFundWindow,text='Fund name: ')
            createFundNameLabel.pack()
            createFundNameInputField = Entry(createFundWindow)
            createFundNameInputField.pack()
            createFundButon = Button(createFundWindow, text='Create new fund', command =lambda: createNewFund(createFundNameInputField.get()))
            createFundButon.pack()
            

        def createNewFund(name):
            global rowCounter, colCounter, withdrawNewFundButton,depositNewFundButton,newFundEntry
            rowCounter+=1
            GUI.newFundLabel = Label(root,text=name+' Fund: ', name=name+'Label')
            GUI.newFundLabel.grid(row=rowCounter, column=0)
            GUI.newFundEntry = Entry(root, name='entry'+name+'Fund')
            GUI.newFundEntry.grid(row=rowCounter, column=1)
            GUI.newFundEntry.insert(0,0)
            GUI.withdrawNewFundButton = Button(root, text='Withdraw Money', name='withdrawButton'+name+'Fund', command=lambda: withdrawNewFund(name))
            GUI.withdrawNewFundButton.grid(row=rowCounter+1, column=0)
            GUI.depositNewFundButton = Button(root, text='Deposit Money', name='depositButton'+name+'Fund',command=lambda: depositNewFund(name))
            GUI.depositNewFundButton.grid(row=rowCounter+1, column=1)
            GUI.entryLabel=Label(root, text='       ')
            GUI.entryLabel.grid(row=rowCounter+2, column = 0)
            fundsAttributes.append(GUI.newFundLabel)
            fundsAttributes.append(GUI.newFundEntry)
            fundsAttributes.append(GUI.withdrawNewFundButton)
            fundsAttributes.append(GUI.depositNewFundButton)

            fundData = {
                str(name)+'Fund':0
            }
            jsonFileFundHolder =open(name+'Fund.json', 'w+')
            json.dump(fundData, jsonFileFundHolder, indent=6)

        def deleteFund(name):
            nameLabel = '.'+name+'Label'
            entryName = '.'+'entry'+name+'Fund'
            withdrawButtonName = '.'+'withdrawButton'+name+'Fund'
            depositButtonName = '.'+'depositButton'+name+'Fund'
            for i in fundsAttributes:
                
                if(str(i)==str(nameLabel)):
                    i.destroy()
                if(str(i)==str(entryName)):
                    i.destroy()
                if(str(i)==str(withdrawButtonName)):
                    i.destroy()
                if(str(i)==str(depositButtonName)):
                    i.destroy()

        def deleteFundWindow():
            deleteFundWindow = Toplevel()
            deleteFundWindow.geometry('400x500')

            deleteFundNameLabel = Label(deleteFundWindow,text='Fund name: ')
            deleteFundNameLabel.pack()
            deleteFundNameInputField = Entry(deleteFundWindow)
            deleteFundNameInputField.pack()
            deleteFundButon = Button(deleteFundWindow, text='Delete fund', command =lambda: deleteFund(deleteFundNameInputField.get()))
            deleteFundButon.pack()

        def manageNewFund(name):
            savedMoney=[]
            data_file=open(name+'Fund.json')
            loaded_data = json.load(data_file)
            pairs = loaded_data.items()
            for key,value in pairs:
                print(value)

        def withdrawNewFund(name):
            pass

        def depositNewFund(name):
            fundData = {
                str(name)+'Fund': GUI.newFundEntry.get()
            }
            data_file = open(name+'Fund.json','w')
            json.dump(fundData, data_file, indent=6)

        #CREATE NEW FUND BUTTON
        createFundButton = Button(text='Create a new fund', command=createFundWindow)
        createFundButton.grid(row=2, column=5)

        #DELETE FUND BUTTON
        deleteFundButton = Button(text='Delete a fund', command=deleteFundWindow)
        deleteFundButton.grid(row=2, column=6)

GUI.emFundGUI()
GUI.thingsFundGUI()
GUI.optionsGUI()


root.mainloop()