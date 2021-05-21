import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=os.getenv('PASSWORD'),
  database="Mmanager"
)