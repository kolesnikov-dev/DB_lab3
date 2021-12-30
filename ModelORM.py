import random

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Sequence, delete, insert, update, select
from sqlalchemy import String, Integer, Float, Boolean, Column
from sqlalchemy.orm import sessionmaker

import Database
import time

import ORMModels
from ORMModels import *

Tables = {
    1: 'Products',
    2: 'Sellers',
    3: 'Clients',
    4: 'Prices',
    5: 'ClientsProducts',
    6: 'SellersProducts'
}

class Model:
    @staticmethod
    def existingtable(table):
        if str(table).isdigit():
             table = int(table)
             cons = True
             while cons:
                if table == 1 or table == 2 or table == 3 or table == 4 or table == 5 or table == 6:
                   return table
                else:
                   print('///Try again.')
                   return 0
        else:
             print('Try again')
             return 0

    @staticmethod
    def getTableClass(choice):
        if choice == 1:
            return Product
        elif choice == 2:
            return Seller
        elif choice == 3:
            return Client
        elif choice == 4:
            return Price
        elif choice == 5:
            return ClientsProduct
        elif choice == 6:
            return SellersProduct

    @staticmethod
    def outputonetable(table):
        engine = Database.getEngine()
        Session = sessionmaker(bind=engine)
        session = Session()

        return session.query(Model.getTableClass(table)).all()


    @staticmethod
    def insertProduct(f,s,added,notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            subj = Product(name=f, Pricesid=int(s))
            session.add(subj)
            session.commit()
            print(added)
        except:
            print(notice)

    @staticmethod
    def insertSeller(f, s, added, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            subj = Seller(name=f, surname=s)
            session.add(subj)
            session.commit()
            print(added)
        except:
            print(notice)

    @staticmethod
    def insertClient(f,s,p, t,added,notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            subj = Client(Name=f, Surname=s, Patronymic=t, Price=p)
            session.add(subj)
            session.commit()
            print(added)
        except:
            print(notice)

    @staticmethod
    def insertPrice(f,s,t,added,notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            subj = Price(time=t, Clientsid=f, Sellersid=s)
            session.add(subj)
            session.commit()
            print(added)
        except:
            print(notice)

    @staticmethod
    def deleteProduct(idk, delete, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            Product = session.query(ORMModels.Product).where(ORMModels.Product.id == idk).one()
            session.delete(Product)
            session.query(Price).where(Price.id == Product.pricesid).delete()
            session.commit()
            print(delete)
        except:
           print(notice)

    @staticmethod
    def deleteSellers(idk, delete, notice):
        #try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            session.query(Seller).where(Seller.id == idk).delete()
            session.query(Price).where(Price.sellersid == idk).delete()
            session.query(SellersProduct).where(SellersProduct.sellersid == idk).delete()
            session.commit()
            print(delete)
        #except:
           #print(notice)

    @staticmethod
    def deleteClients(idk, delete, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            session.query(Client).where(Client.Id == idk).delete()
            session.query(Price).where(Price.clientsid == idk).delete()
            session.query(ClientsProduct).where(ClientsProduct.clientsid == idk).delete()
            session.commit()
            print(delete)
        except:
            print(notice)

    @staticmethod
    def deletePrices(idk, delete, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            session.query(Price).where(Price.id == idk).delete()
            session.commit()
            print(delete)
        except:
            print(notice)

    @staticmethod
    def UpdateProduct(idk, name, updated, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            Product = session.query(ORMModels.Product).where(ORMModels.Product.id == idk).one()
            Product.name = name
            session.commit()
            print(updated)
        except:
           print(notice)


    @staticmethod
    def UpdateSellers(idk, set1, set2, updated, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            Seller = session.query(ORMModels.Seller).where(ORMModels.Seller.id == idk).one()
            Seller.name = set1
            Seller.surname = set2
            session.commit()
            print(updated)
        except:
           print(notice)

    @staticmethod
    def UpdateClients(idk, name, patronymic, surname, updated, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            Client = session.query(ORMModels.Client).where(ORMModels.Client.Id == idk).one()
            Client.Name = name
            Client.Patronymic = patronymic
            Client.Surname = surname
            session.commit()
            print(updated)
        except:
           print(notice)

    @staticmethod
    def UpdatePrices(idk, date, updated, notice):
        try:
            engine = Database.getEngine()
            Session = sessionmaker(bind=engine)
            session = Session()

            Price = session.query(ORMModels.Price).where(ORMModels.Price.id == idk).one()
            Price.time = date
            session.commit()
            print(updated)
        except:
           print(notice)

    @staticmethod
    def selectionone(timestamp, SellerSurname):
        connect = Database.connect()
        cursor = connect.cursor()
        select = """
        select 
            public."Sellers".name, public."Sellers".surname, 
            public."Clients"."Name", public."Clients"."Surname"
            
            from public."Sellers"
            right join public."Prices" on public."Prices".Sellersid = public."Sellers".id
            left join public."Clients" on public."Prices".Clientsid = public."Clients"."Id"
            
            where public."Prices".time > '{}'
                and public."Sellers".surname like '{}'
        """.format(timestamp, SellerSurname)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        datas = cursor.fetchall()
        print('Time of request {} ms'.format(end))
        print('Selected')
        cursor.close()
        Database.close(connect)
        return datas

    @staticmethod
    def selectiontwo(subj, PriceTime):
        connect = Database.connect()
        cursor = connect.cursor()
        select = """
        select 
            public."Sellers".name, public."Sellers".surname, 
            public."Products".name,
            public."Prices".time
            
            from public."Products"
            join public."Prices"on public."Prices".id = public."Products".Pricesid
            join public."Sellers" on public."Prices".Sellersid = public."Sellers".id
            
            where public."Products".name like '{}'
                and public."Prices".time > '{}'
        """.format(subj, PriceTime)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        datas = cursor.fetchall()
        print('Time of request {} ms'.format(end))
        print('Selected')
        cursor.close()
        Database.close(connect)
        return datas

    @staticmethod
    def selectionthree(SellersS, ClientsS):
        connect = Database.connect()
        cursor = connect.cursor()
        select = """
        select public."Products".name from public."Products"

            join public."Prices"on public."Prices".id = public."Products".Pricesid
            
            join public."SellersProducts" 
                on public."SellersProducts".Productsid = public."Products".id
                and public."SellersProducts".Sellersid = public."Prices".Sellersid
            
            join public."ClientsProducts" 
                on public."ClientsProducts".Productsid = public."Products".id
                and public."ClientsProducts".Clientsid = public."Prices".Clientsid 
            
            join public."Clients" on "ClientsProducts".Clientsid = public."Clients"."Id"
            join public."Sellers" on public."SellersProducts".Sellersid = public."Sellers".id
                
            where public."Sellers".surname like '{}'
                and public."Clients"."Surname" like '{}'
                
            group by public."Products".name
        """.format(SellersS, ClientsS)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        datas = cursor.fetchall()
        print('Time of request {} ms'.format(end))
        print('Selected')
        cursor.close()
        Database.close(connect)
        return datas




    @staticmethod
    def randomik(table, kolvo):
            connect = Database.connect()
            cursor = connect.cursor()
            check = True
            while check:
                if table == 1:
                    res = 0
                    while (True):
                        insert = "INSERT INTO public.\"Products\"(Name, PricesID) select chr(trunc(65 + random()*26)::int)||chr(trunc(65 + r" \
                             "andom()*26)::int)," \
                             "(select id from public.\"Prices\" order by random() limit 1)" \
                             " from generate_series(1,{})".format(kolvo)
                        cursor.execute(insert)
                        res = res + 1
                        if(res == int(kolvo)):
                            break
                    check = False
                elif table == 2:
                    res = 0
                    while (True):
                        insert = "INSERT INTO public.\"Sellers\"(Name, Surname) select chr(trunc(65 + random()*26)::int)||chr(trunc(65 + r" \
                             "andom()*26)::int), " \
                             "chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int) " \
                             "from generate_series(1,{})".format(kolvo)
                        cursor.execute(insert)
                        res = res + 1
                        if(res == int(kolvo)):
                            break
                    check = False
                elif table == 3:
                    res = 0
                    while (True):
                        insert = "INSERT INTO public.\"Clients\"(\"Name\", \"Surname\", \"Patronymic\") select chr(trunc(65 + random()*26)::int)||chr(trunc(65 + r" \
                             "andom()*26)::int), " \
                             "chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int), " \
                             "chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int)" \
                             "from generate_series(1,{})".format(kolvo)
                        cursor.execute(insert)
                        res = res + 1
                        if(res == int(kolvo)):
                            break
                    check = False
                elif table == 4:
                    res = 0
                    while (True):
                        insert = "INSERT INTO public.\"Prices\"(Time, ClientsID, SellersID) values(" \
                                 "(select NOW() + (random() * (NOW()+'90 days' - NOW())) + '{} days')," \
                                 "(select \"Id\" from public.\"Clients\" order by random() limit 1)," \
                                 "(select id from public.\"Sellers\" order by random() limit 1))".format(kolvo)
                        cursor.execute(insert)
                        res = res + 1
                        if (res == int(kolvo)):
                            break
                    check = False
                elif table == 5:
                    res = 0
                    while (True):
                        insert = "INSERT INTO public.\"ClientsProducts\"(ClientsID, ProductsID) values(" \
                                 "(select \"Id\" from public.\"Clients\" order by random() limit 1)," \
                                 "(select id from public.\"Products\" order by random() limit 1))".format(kolvo)
                        cursor.execute(insert)
                        res = res + 1
                        if (res == int(kolvo)):
                            break
                    check = False
                elif table == 6:
                    res = 0
                    while (True):
                        insert = "INSERT INTO public.\"SellersProducts\"(SellersID, ProductsID) values(" \
                                 "(select id from public.\"Sellers\" order by random() limit 1)," \
                                 "(select id from public.\"Products\" order by random() limit 1))".format(kolvo)
                        cursor.execute(insert)
                        res = res + 1
                        if (res == int(kolvo)):
                            break
                    check = False
            print(Tables[table])
            print("SQL query => ", insert)
            connect.commit()
            print('Inserted randomly')
            cursor.close()
            Database.close(connect)