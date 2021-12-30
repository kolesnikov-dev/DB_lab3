import psycopg
import Database
from sqlalchemy import engine
from View import Menu

try:
    Database.initEngine()
    Menu.mainmenu()
except (Exception , psycopg.Error) as error:
        print ("Database Error: ",error)
finally:
    print("Database connection is closed")
    Database.getEngine()