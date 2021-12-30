import psycopg2
import sqlalchemy

Engine = None

def initEngine():
    global Engine
    Engine = sqlalchemy.create_engine("postgresql+psycopg2://itqsairb:WM9zBNLbxiOlMwNRozSINkOLX0c01ppO@abul.db.elephantsql.com/itqsairb")

def getEngine():
    global Engine
    return Engine

def connect():
    return psycopg2.connect(
        user="itqsairb",
        password="WM9zBNLbxiOlMwNRozSINkOLX0c01ppO",
        host="abul.db.elephantsql.com",
        port="5432",
        database="itqsairb"
    )

def close(connect):
    connect.commit()
    connect.close()