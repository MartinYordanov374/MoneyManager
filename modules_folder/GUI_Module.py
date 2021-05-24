from tkinter import *
import Data_Module
import EmFund_Module
import MiscFund_Module
import os
import json
from datetime import date
from Database_Module import mydb
from Data_Module import *
root = Tk()

root.title('MoneyManager')
root.geometry("1100x700")

class GUI():

    global rowCounter, colCounter
    global fundsAttributes
    fundsAttributes=[]
    rowCounter = 5
    colCounter = 0
    emFundBox = Entry(root, state='normal')
    emFundBox.grid(row=0, column=1)

    def emFundGUI():
        GUI.emergencyFundLabel = Label(root, text='Emergency Fund:').grid(row=0, column=0)

        #TEXTBOX - EMERGENCY FUND
        GUI.emFundBox = Entry(root, state='normal')
        GUI.emFundBox.grid(row=0, column=1)
        GUI.emFundBox.insert(0,Data_Module.savedEmFundMoney)

        #WITHDRAW FROM EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW

        GUI.emFundWithdrawButton = Button(root, text='Withdraw money', command=EmFund_Module.EmFund.withdrawMoneyEmFund).grid(row=1, column=0)

        #ADD TO EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD

        GUI.emFundAddButton = Button(root, text='Deposit money', command=EmFund_Module.EmFund.addMoneyEmFund).grid(row=1, column=1)

    def thingsFundGUI():
        #BUTTON LABEL - THINGS
        GUI.thingsLabel = Label(root, text='Miscellanious Fund: ')
        GUI.thingsLabel.grid(row=2, column=0)
        #TEXTBOX - THINGS FUND
        GUI.thingsInputBox = Entry(root)
        GUI.thingsInputBox.grid(row=2, column=1)
        GUI.thingsInputBox.insert(0, Data_Module.savedMiscMoney)
        #WITHDRAW FROM THINGS FUNDS -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW
        GUI.withdrawThingsButton = Button(root, text='Withdraw Money', command=MiscFund_Module.MiscFund.withdrawMoneyMiscFund)
        GUI.withdrawThingsButton.grid(row=3, column=0)

        #ADD TO THINGS FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD
        GUI.depositThingsButton = Button(root, text='Deposit Money', command=MiscFund_Module.MiscFund.addMoneyMiscFund)

        GUI.depositThingsButton.grid(row=3, column=1)

    def optionsGUI():
        #SHOW HISTORY OF WITHDRAWALS AND DEPOSITS 
        showHistoryButton = Button(root, text='show withdraw/deposit history', command=Data_Module.DataOperations.readTransactionHistory)
        emptyLabel = Label(root, text='     ').grid(row=2, column=3)

        showHistoryButton.grid(row=2, column=4)


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

            todayDate = date.today()  
            queryCursor = mydb.cursor()
            queryTwo = 'SELECT COUNT(*) FROM FundsArchive WHERE fundname=%s'
            valueCheck = (name,)
            queryCursor.execute(queryTwo,valueCheck)
            result = queryCursor.fetchall()
            if(result==[(0,)]):
                queryCursor = mydb.cursor()
                queryOne ='INSERT INTO FundsArchive (fundname, FundsDate) VALUES (%s,%s)'
                val=(name, str(todayDate))
                queryCursor.execute(queryOne,val)
                mydb.commit()
                GUI.newFundLabel = Label(root,text=name+' Fund: ', name=name+'Label')
                GUI.newFundLabel.grid(row=rowCounter, column=0)
                GUI.newFundEntry = Entry(root, name='entry'+name+'Fund')
                GUI.newFundEntry.grid(row=rowCounter, column=1)
                GUI.newFundEntry.insert(0,0)
                GUI.withdrawNewFundButton = Button(root, text='Withdraw Money', name='withdrawButton'+name+'Fund', command=lambda: showCustomFund.withdrawNewFund(name))
                GUI.withdrawNewFundButton.grid(row=rowCounter+1, column=0)
                GUI.depositNewFundButton = Button(root, text='Deposit Money', name='depositButton'+name+'Fund',command=lambda: showCustomFund.depositNewFund(name))
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
                createFundWindow = Toplevel()
                createFundWindow.geometry('800x50')

                createFundNameLabel = Label(createFundWindow,text='In order for your newly created fund to function properly you may have to restart your application ')
                createFundNameLabel.pack()
            else:
                errorScreen = Toplevel()
                errorMessage = Label(errorScreen, text='ERROR - FUND ALREADY EXISTS')
                errorMessage.pack()

           
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
            
            deleteCursor = mydb.cursor()
            deleteSQL = 'DELETE FROM FundsArchive WHERE fundname=%s'
            val=(name,)
            deleteCursor.execute(deleteSQL,val)
            mydb.commit()
            
            os.remove(name+'Fund.json')

        def deleteFundWindow():
            deleteFundWindow = Toplevel()
            deleteFundWindow.geometry('400x500')

            deleteFundNameLabel = Label(deleteFundWindow,text='Fund name: ')
            deleteFundNameLabel.pack()
            deleteFundNameInputField = Entry(deleteFundWindow)
            deleteFundNameInputField.pack()
            deleteFundButon = Button(deleteFundWindow, text='Delete fund', command =lambda: deleteFund(deleteFundNameInputField.get()))
            deleteFundButon.pack()

        #CREATE NEW FUND BUTTON
        createFundButton = Button(text='Create a new fund', command=createFundWindow)
        createFundButton.grid(row=2, column=5)

        #DELETE FUND BUTTON
        deleteFundButton = Button(text='Delete a fund', command=deleteFundWindow)
        deleteFundButton.grid(row=2, column=6)

    def showCustomFund(name, rowCountDynamic, colCountDynamic):

            def withdrawNewFund(name):
                global newFundWithdrawMoneyField,rowCounter, colCounter
                GUI.newFundWithdrawScreen = Toplevel()
                GUI.newFundWithdrawScreen.title('Withdraw Money - '+name+' Fund')
                GUI.newFundWithdrawScreen.geometry("475x500")
                withdrawMoneyPromptMessage = Label(GUI.newFundWithdrawScreen,text='How much money would you like to withdraw from your'+name+' Fund?')
                withdrawMoneyPromptMessage.grid(row=0, column=0)
                GUI.newFundWithdrawMoneyField= Entry(GUI.newFundWithdrawScreen, name=name+'WithdrawField')
                GUI.newFundWithdrawMoneyField.grid(row=1, column=0, ipadx=130)
                finishAddingButton = Button(GUI.newFundWithdrawScreen, text='Withdraw money from your '+name+' fund',width=50, command=lambda: confirmWithdrawNewFund(name,GUI.newFundWithdrawMoneyField.get())).grid(row=2,column=0)
     
            def confirmWithdrawNewFund(name, amount):
            
                currentFundMoney = int(root.nametowidget('entry'+name+'Fund').get())
                moneyToWithdraw = int(amount)
                print(currentFundMoney, '->', moneyToWithdraw)
                if(len(amount)>=0 and moneyToWithdraw<=currentFundMoney):
                    fundData = {
                        str(name)+'Fund': currentFundMoney-moneyToWithdraw
                    }
                    data_file = open(name+'Fund.json','w')
                    json.dump(fundData, data_file, indent=6)

                    root.nametowidget('entry'+name+'Fund').delete(0,END)

                    root.nametowidget('entry'+name+'Fund').insert(0,currentFundMoney-moneyToWithdraw)
                else:
                    errorScreen = Toplevel()
                    errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
                    errorMessage.pack()

            def depositNewFund(name):
                global newFundMoneyField
                GUI.newFundAddScreen = Toplevel()
                GUI.newFundAddScreen.title('Deposit Money - '+name+' Fund')
                GUI.newFundAddScreen.geometry("475x500")
                addMoneyPromptMessage = Label(GUI.newFundAddScreen,text='How much money would you like to deposit to your'+name+' Fund?')
                addMoneyPromptMessage.grid(row=0, column=0)
                GUI.newFundMoneyField= Entry(GUI.newFundAddScreen)
                GUI.newFundMoneyField.grid(row=1, column=0, ipadx=130)
                finishAddingButton = Button(GUI.newFundAddScreen, text='Deposit money to your'+name+' fund',width=50, command=lambda: confirmDepositNewFund(name,GUI.newFundMoneyField.get())).grid(row=2,column=0)
                
            def confirmDepositNewFund(name, amount):
                #Get amount before deposit
                currentMoney = root.nametowidget('entry'+name+'Fund').get()
                #Amount entered in the deposit window
                depositedMoney = amount
                #Calculate total
                totalMoney = int(depositedMoney)+int(currentMoney)
                print(amount,' + ',currentMoney,' = ',totalMoney)
                root.nametowidget('entry'+name+'Fund').delete(0,END)
                root.nametowidget('entry'+name+'Fund').insert(0,totalMoney)
                saveDataCustom(name,totalMoney)


            GUI.newFundLabel = Label(root,text=name+' Fund: ', name=name+'Label')
            GUI.newFundLabel.grid(row=rowCountDynamic+1, column=0)
            GUI.newFundEntry = Entry(root, name='entry'+name+'Fund')
            GUI.newFundEntry.grid(row=rowCountDynamic+1, column=1)
            GUI.withdrawNewFundButton = Button(root, text='Withdraw Money', name='withdrawButton'+name+'Fund', command=lambda: withdrawNewFund(name))
            GUI.withdrawNewFundButton.grid(row=rowCountDynamic+1, column=2)
            GUI.depositNewFundButton = Button(root, text='Deposit Money', name='depositButton'+name+'Fund',command=lambda: depositNewFund(name))
            GUI.depositNewFundButton.grid(row=rowCountDynamic+1, column=3)

            fundsAttributes.append(GUI.newFundLabel)
            fundsAttributes.append(GUI.newFundEntry)
            fundsAttributes.append(GUI.withdrawNewFundButton)
            fundsAttributes.append(GUI.depositNewFundButton)
            def saveDataCustom(name,amount):
                #Generate the fund JSON data
                fundData = {
                    name+"Fund": int(amount)

                }
                #Open the json file
                jsonFileFundHolder =open(name+'Fund.json', 'w+')
                #Write to the JSON file
                json.dump(fundData,jsonFileFundHolder,indent=6)
                jsonFileFundHolder.close()
            #Load data from json files
            def loadDataCustom(name):
                savedMoney=[]
                data_file_custom=open(name+'Fund.json')
                loaded_data_custom = json.load(data_file_custom)
                pairs = loaded_data_custom.items()
                for key,value in pairs:
                    #Save data to list
                    savedMoney.append(value)
                savedTotalFundMoney = savedMoney[0]
                root.nametowidget('entry'+name+'Fund').insert(0,savedTotalFundMoney)
                data_file_custom.close()
                #Send fund name and amount data to the saveData function
                # saveDataCustom(name,savedTotalFundMoney)

            loadDataCustom(name)
        
            DataOperations.readCustomFundData(name)
            

