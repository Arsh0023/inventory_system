import os
import sqlite3

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#db_path = os.path.join(BASE_DIR, "inventory.db")
#conn = sqlite3.connect(db_path) #this will make an in memory database.
conn = sqlite3.connect(':memory:')
c = conn.cursor() #so that we can execute sql commands.

if not os.path.isfile('inventory.db'):
    c.execute("""CREATE TABLE inventory (
        Id integer,
        name text,
        price real,
        stock real
        )""")

    conn.commit() #this is finally to commit the changes.

#conn.close() #to close the connection with the database.

class Item():
    def __init__(self,Id=None,name=None,price=None,stock=None):
        self.Id = Id
        self.name = name
        self.price = price
        self.stock = stock

    def print_item(self):
        print(f'{self.name} with an Id of {self.Id} and Price of {self.price}')

class Inventory():
    """this is the class which will interact with the database"""
    
    @staticmethod
    def add_item(item):
        with conn:
            c.execute("INSERT INTO inventory VALUES (?,?,?,?)",(item.Id,item.name,item.price,item.stock))

    @staticmethod
    def remove_item(item):
        with conn:
            c.execute("DELETE from inventory WHERE Id = ?",(item.Id,))

    @staticmethod
    def add_stock(item):
        c.execute("Select * FROM inventory WHERE Id = ?",(item.Id,))
        it = c.fetchone()
        a,b,z,q = it
        net = q+item.stock
        with conn:
            c.execute("UPDATE inventory SET stock = ? WHERE Id = ?",(net,item.Id,))

    @staticmethod
    def remove_stock(item):
        c.execute("Select * FROM inventory WHERE Id = ?",(item.Id,))
        it = c.fetchone()
        a,b,z,q = it
        net = q-item.stock
        with conn:
            c.execute("UPDATE inventory SET stock = ? WHERE Id = ?",(net,item.Id))
    
    @staticmethod
    def print_inventory():
        #this should query for all the items in a databse and print them
        c.execute("Select * FROM inventory")
        objs = c.fetchall()
        for ent in objs:
            i,n,s,p = ent
            print(f'{i} - {n} - {p} - {s}')
        pass


def main():
    print('Hello welcome to the inventory,what would you like to do today')
    print('Please enter a number between 1-6: ')
    print(' 1. Add an Item \n 2. Remove an Item \n 3. Increase Stock \n 4. Decrease Stock \n 5. Show inventory \n 6. Exit')
    inp = int(input())
    print()

    while(inp != 6):
        if inp == 1:
            #add an item to db
            #if the item already exists then make changes to it
            Id = int(input('Please Enter the Id of the item you would like to add: '))
            name = input('Please Enter the name of the item you would like to add: ')
            price = float(input('Please Enter the price of the item you would like to add: '))
            initial_stock = int(input('Please Enter the initial stock of the item you would like to add: '))
            item = Item(Id,name,price,initial_stock)

            Inventory.add_item(item)
            
            print(f'Added {initial_stock}',end=" ")
            item.print_item()
            
        if inp == 2:
            Id = int(input('Please Enter the Id of the item you would like to delete: '))
            item = Item(Id=Id)
            Inventory.remove_item(item)
            print('Item removed from the inventory')

        if inp == 3:
            #increase stock
            Id = int(input('Please Enter the Id of the item you would like to increase stock for: '))
            quantity = int(input('How many would you like to add: '))
            item = Item(Id= Id, stock=quantity)
            Inventory.add_stock(item)
            print(f'{quantity} quantity has been added to product Id = {Id}')

        if inp == 4:
            #decrease stock
            Id = int(input('Please Enter the Id of the item you would like to decrease stock for: '))
            quantity = int(input('How many would you like to decrease: '))
            item = Item(Id = Id , stock=quantity)
            Inventory.remove_stock(item)
            print(f'{quantity} quantity has been removed from product Id = {Id}')

        if inp == 5:
            Inventory.print_inventory()
        
        print()
        print('Hello welcome to the inventory,what would you like to do today')
        print('Please enter a number between 1-6: ')
        print(' 1. Add an Item \n 2. Remove an Item \n 3. Increase Stock \n 4. Decrease Stock \n 5. Show inventory \n 6. Exit')

        inp = int(input())

if __name__ == '__main__':
    main()



