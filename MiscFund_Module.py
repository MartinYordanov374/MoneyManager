import GUI_Module
from GUI_Module import Toplevel, Listbox, END, Button, Entry, Label
import Data_Module
from Database_Module import mydb
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
            formerAmount = int(GUI_Module.GUI.thingsInputBox.get())
            GUI_Module.GUI.thingsInputBox.delete(0,END)
            GUI_Module.GUI.thingsInputBox.insert(0,currAmount+formerAmount)
            Data_Module.DataOperations.saveData()
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
        currentFundMoney = int(GUI_Module.GUI.thingsInputBox.get())
        moneyToWithdraw = int(amount)
        if(len(amount)>=0 and moneyToWithdraw<=currentFundMoney):
            GUI_Module.GUI.thingsInputBox.delete(0,END)
            GUI_Module.GUI.thingsInputBox.insert(0,currentFundMoney-moneyToWithdraw)
            Data_Module.DataOperations.saveData()

            queryCursor = mydb.cursor()
            queryOne ='INSERT INTO TransactionHistory (type, amount) VALUES (%s, %s)'
            val=('withdraw', amount)
            queryCursor.execute(queryOne,val)
            mydb.commit()

        else:
            errorScreen = Toplevel()
            errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
            errorMessage.pack()