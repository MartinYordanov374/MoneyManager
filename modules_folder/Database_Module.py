import mysql.connector
from dotenv import load_dotenv
import os

import sqlite3

mydb = sqlite3.connect('ManagerDB.db')
mydb.execute('''CREATE TABLE IF NOT EXISTS FundsArchive(
  ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  fundname CHAR(20),
  fundsDate CHAR(120))''')

mydb.execute('''CREATE TABLE IF NOT EXISTS TransactionHistory(
  ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  type CHAR(120),
  amount CHAR(120))''')
