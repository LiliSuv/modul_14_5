import sqlite3
import vit


def initiate_db(id,title,description,price,foto):
    connection = sqlite3.connect ("products.db")
    cursor = connection.cursor ()

    cursor.execute ('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT ,
    price INTEGER,
    foto INTEGER
    
    )
    ''')
    cursor. execute( 'INSERT INTO Products (id,title,description,price,foto) VALUES (?,?,?,?,?)',(f"{id}",f"{title}",
                                                                                f"{description}", f"{price}руб",f'fls/{id}.PNG'))
    connection.commit ()
    connection.close ()
#initiate_db (1,'Витамины группы B NOW',f"{vit.v1}",3008,1)
#initiate_db (2,'2Витаминный комплекс Now Foods B-50',f"{vit.v2}",1049,2)
#initiate_db (3,'Now foods Vitamin D-3 2000 ME',f"{vit.v3}",563, 3)
#initiate_db (4,'4Now Mega D-3 & MK-7 60',f"{vit.v4}",1211,4)


def get_all_products():
    connection = sqlite3.connect ('products.db')
    cursor = connection.cursor ()
    cursor.execute ("SELECT title, description, price,foto,id FROM Products")
    product = cursor.fetchall ()
    connection.commit ()
    connection.close ()
    return product


def initiate_db_user():
    connection = sqlite3.connect ("bdu.db")
    cursor = connection.cursor ()
    cursor.execute ('''
                CREATE TABLE IF NOT EXISTS User(
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL ,
                age INTEGER ,
                balance INTEGER
                )
                ''')
    connection.commit ()
    connection.close ()


def all_user(username, email, age):
    connection = sqlite3.connect ("bdu.db")
    cursor = connection.cursor ()
    cursor.execute ('INSERT INTO User (username,email,age,balance ) VALUES (?,?,?,?)', (f'{username}', f'{email}', f'{age}',1000))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("bdu.db")
    cursor = connection.cursor()
    user = cursor.execute ("SELECT * FROM User WHERE username = ?", (username,))
    if user.fetchone() is None:
        return False
    else:
        return True

initiate_db_user()



