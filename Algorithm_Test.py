import spidev
import sqlite3
from sqlite3 import Error
import datetime

#SPI Configurations
def Start_Spi():
    bus = 0
    device = 0
    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = 5000
    spi.mode = 0b00
    
    return spi 

#Create Database connection function 
def Create_DB_Connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn

#Create New Table in database
def Create_Table(conn, Create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(Create_table_sql)
    except Error as e:
        print(e)    

#Insert data into the table
def Insert_Data(conn, InsertCmd, InsertData):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    """sql = ''' INSERT INTO BatLog(Timestamp,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''' """
    try:
        cur = conn.cursor()
        cur.execute(InsertCmd, InsertData)
        conn.commit()
    except Error as e:
        print(e)

    return cur.lastrowid

def main():
    #Redis Connection Block


    #Open SPI connection
    spi = Start_Spi()

    #Database Location
    Database = r"/home/snow/Database_Test/Test_Dummy.db"
    
    #Create a connection to Database
    conn = Create_DB_Connection(Database)
    
    #Create a table in Database with Specific name
    #String Maniplulation Block
    Create_Table_SQL_CMD = """ CREATE TABLE IF NOT EXISTS BatLog (
                                        id integer PRIMARY KEY,
                                        Timestamp text NOT NULL,
                                        V1 real,V2 real,V3 real,V4 real,V5 real,V6 real,V7 real,V8 real,V9 real,V10 real,
                                        T1 real,T2 real,T3 real,T4 real,T5 real,T6 real,T7 real,T8 real,T9 real,T10 real,
                                        C1 real,C2 real,C3 real,C4 real,C5 real,C6 real,C7 real,C8 real,C9 real,C10 real,
                                        I1 real,I2 real,I3 real,I4 real,I5 real,I6 real,I7 real,I8 real,I9 real,I10 real,
                                        A1 real,A2 real,A3 real,A4 real,A5 real,A6 real,A7 real,A8 real,A9 real,A10 real
                                    ); """

    Insert_Data_SQL_CMD = ''' INSERT INTO BatLog(Timestamp,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    i = 1
    with conn:
        #Create Table command execution
        Create_Table(conn, Create_Table_SQL_CMD)


        while i<=5:
            #SPI data retrieve code
            Read_BMS_Command = [0x2]
            
            spi.writebytes(Read_BMS_Command)
            Dummy_Read = spi.readbytes(1)
            Dummy = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            Rcvd_Data = spi.xfer(Dummy)
            
            #Copy SPI Output list to newlist
            BMS_Data = Rcvd_Data.copy()
            
            #Get Timestamp
            Time = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S') 
            BMS_Data.insert(0, Time)
            BMS_Store_Data = tuple(BMS_Data)

            #Store Data onto Database
            Insert_Data(conn, Insert_Data_SQL_CMD, BMS_Store_Data)

            #BMS Algorithm Start


            #BMS Algorithm End
            i+=1
    
    #Charging Completion Block
     #Sleep process for some time

     #After Charging Testing


    #Stop Charging
    #Close SPI connection
    spi.close()
    #Close connection to database
    conn.close()




            
if __name__ == '__main__':
    main()

    



    