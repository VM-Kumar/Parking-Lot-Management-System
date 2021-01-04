# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:52:02 2020

@author: venkatesh

"""
import mysql.connector as mysql
import sys
import datetime
from datetime import *
from dateutil.relativedelta import relativedelta


host = "localhost"
user = "root"
passwd = "abcd1234"

#Establishes connection to the server and creates a database called "project"
try : 
    server_con = mysql.connect(
        host= host,
        user= user,
        passwd= passwd,
        database="project"
         )
    print("Connection to Database Established")
    
except mysql.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))

mycursor = server_con.cursor()

############################### FUNCTIONS ##################################
def AddLot(name,address,n_spaces,start_n,zone):
     
    insert_stmt1 = f"INSERT INTO p_lots(name,address,zone) VALUES('{name}','{address}','{zone}')"
    mycursor.execute(insert_stmt1)
    server_con.commit()
    
    for i in range(start_n,start_n+n_spaces):
        insert_stmt2 = f"INSERT INTO spaces(name,sid,space_type) VALUES('{name}',{i},'R')"
        mycursor.execute(insert_stmt2)
        server_con.commit()

def AssignZoneToLot(name,zones):
    dic = {'A':1,'B':1,'C':1,'D':1,'AS':2,'BS':2,'CS':2,'DS':2,'V':3 }
    individual_zone= zones.split("/")
    
    for zone in individual_zone:
        if zone not in dic:
            print(f"You have entered Invalid Zones :{zone}")
            return zone
    
    update_stmt = f"UPDATE p_lots SET zone = '{zones}' WHERE name = '{name}'"
    mycursor.execute(update_stmt)
    server_con.commit()
   

def AssignTypeToSpace(name,start_n,end_n,p_type):
    
    dic = {'R':0,'V':1,'E':2,'H':3}
    if p_type not in dic:
        print(f"You have entered an Invalid space type : {p_type} ")
        return p_type
    
    for i in range(start_n,end_n+1):
        update_stmt =  f"UPDATE spaces SET space_type = '{p_type}' WHERE name = '{name}' AND sid = {i}"
        mycursor.execute(update_stmt)
        server_con.commit()

def AddVehicle(license_no,manufacturer,model,year,color):
    try:
        stmt = f"INSERT INTO vehicle_info(license_no,manufacturer,model,year,color) VALUES('{license_no}','{manufacturer}','{model}','{year}','{color}')"
        mycursor.execute(stmt)
        server_con.commit()
    except mysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))


'''#Expiration time is dependent on zone_id,start_date'''
def IssuePermit(unique_permit_id,zone_id,license_no,start_date,space_type,univ_id,manufacturer,model,year,color):
    
    dic = {'A':1,'B':1,'C':1,'D':1,'AS':2,'BS':2,'CS':2,'DS':2,'V':3 }
    
    #Checks Validity of Zone_id
    if zone_id not in dic:
            print(f"You have entered Invalid Zones :{zone_id}")
            return 0
        
    #To check if it is an Employee or Student to calculate Expiration Date
    if dic[zone_id] == 1:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        expiration_date_obj = start_date_obj + relativedelta(years=1)
        expiration_date = datetime.strftime(expiration_date_obj, '%Y-%m-%d')
    
    elif dic[zone_id] == 2:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        expiration_date_obj = start_date_obj + relativedelta(months=4)
        expiration_date = datetime.strftime(expiration_date_obj, '%Y-%m-%d')
    
    else: 
        print("Invalid Zone Entry") 
        return 0
    
    
    stmt = f"INSERT INTO non_visitor_permits(unique_permit_id,zone_id,license_no,start_date,expiration_date,space_type,univ_id) VALUES('{unique_permit_id}','{zone_id}','{license_no}','{start_date}','{expiration_date}','{space_type}','{univ_id}')"
    mycursor.execute(stmt)
    server_con.commit()
    
    AddVehicle(license_no, manufacturer, model, year, color)
       


def GetVisitorPermit (UNIQUE_PERMIT_ID,LICENSE_NO,START_DATE,START_TIME,DURATION,LOT,SPACE_TYPE,SPACE_NO,manufacturer, model, year, color):
    insert_stmt = "INSERT INTO VISITOR_PERMITS(UNIQUE_PERMIT_ID ,LICENSE_NO,START_DATE,EXPIRATION_DATE,START_TIME,DURATION,EXPIRATION_TIME,LOT,SPACE_TYPE,SPACE_NO) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    D=START_DATE.split("-")
    T=START_TIME.split(":")
    End=datetime(int(D[0]),int(D[1]),int(D[2]),int(T[0]),int(T[1]))+timedelta(hours=int(DURATION))
    EXPIRATION_DATE=End.strftime("%Y-%m-%d")
    EXPIRATION_TIME=End.strftime("%H:%M")
    
    DURATION = datetime(1,1,1,int(DURATION),0)
    DURATION = DURATION.strftime("%H:%M")
    
    info=(UNIQUE_PERMIT_ID,LICENSE_NO,START_DATE,EXPIRATION_DATE,START_TIME,DURATION,EXPIRATION_TIME,LOT,SPACE_TYPE,SPACE_NO)
    mycursor.execute(insert_stmt,info)
    server_con.commit()
    
    AddVehicle(LICENSE_NO, manufacturer, model, year, color)


############################### POPULATING TABLES #####################################

#Adding Lots
AddLot("Freedom Lot", "2105 Daniel Allen St, NC 27505", 150, 1, "A")
AddLot("Premiere Lot", "2108 McKent St, NC 27507", 200, 1, "A")
AddLot("Justice Lot", "2704 Ben Clark St, NC 26701 ", 175, 1, "AS")

#Assigning Zones
AssignZoneToLot("Freedom Lot", "A/B/C/D")
AssignZoneToLot("Premiere Lot", "A/B/C/D/AS/BS/CS/DS/V")
AssignZoneToLot("Justice Lot", "AS/BS/CS/DS/V")

#Assigning Space type
AssignTypeToSpace("Premiere Lot", 200, 200, "V")
AssignTypeToSpace("Justice Lot", 150, 175, "V")
AssignTypeToSpace("Justice Lot", 151, 155, "H")
AssignTypeToSpace("Justice Lot", 172, 175, "E")


#Populating NonVisitors
IssuePermit('20B0001B','B','VTZ87543','2020-08-10','E','1007999','Nissan','LEAF','2018','Black')
IssuePermit('20CS001C','CS','UGB9020','2020-08-15','H','1006003','Chevrolet','Cruze','2014','Silver')
IssuePermit('20D0021D','D','TIR3487','2020-07-10','R','1006020','BMW','X5','2017','White')
IssuePermit('20AS016S','AS','NEV9889','2020-09-01','R','1006135','Hyundai','Elantra','2011','Red')
IssuePermit('20A0052A','A','KTP2003','2020-07-29','R','1006022','Acura','RDX','2009','Black')
mycursor.execute("INSERT INTO NON_VISITOR_PERMITS VALUES('20D0021D','2','D','RPU1824','2020-07-10','2021-07-09','00:00','23:59','R','1006020')")


#Populating Visitors:
GetVisitorPermit('20V0001A','CDF5731','2020-08-12','14:00','2','Premiere Lot','R','200','Toyota','Camry','2018','Red')
GetVisitorPermit('20V0012B','TRK1093','2020-08-14','11:00','3','Justice Lot','R','160','Kia','Rio','2017','Blue')
GetVisitorPermit('20V0015J','UGY9123','2020-08-17','10:10','2','Justice Lot','H','151','Nissan','Maxima','2015','Black')
GetVisitorPermit('20V0021L','AKL1732','2020-08-17','11:45','1','Justice Lot','E','173','Tesla','Model X','2019','Silver')
GetVisitorPermit('20V0026P','UWA1118','2020-08-19','14:50', '2','Justice Lot','H','153','Audi','Q3','2016','White')
GetVisitorPermit('20V0025B','TRK1093','2020-09-21','9:30', '4','Premiere Lot','R','200','Kia','Rio','2017','Blue')

insert_stmt = "INSERT INTO CITATIONS(LICENSE_NO,MODEL,COLOR,ISSUE_DATE,LOT,TIME,VIOLATION_CATEGORY,FEE,DUE_DATE,STATUS) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
info = [('TRK1093','Rio','Blue','2020-08-14','Justice Lot','14:40','Expired Permit','25','2020-09-13','Paid'),
('UGY9123','Maxima','Black','2020-08-17','Justice Lot','12:55','Expired Permit','25','2020-09-16','Unpaid'),
('AKL1732','Model X','Silver','2020-08-17','Justice Lot','13:00','Expired Permit','25','2020-09-16','Unpaid'),
('NEV9889','Elantra','Red','2020-09-10','Justice Lot','15:50','Invalid Permit','20','2020-10-09','Unpaid'),
('PTL5642','Sentra','Black','2020-09-14','Freedom Lot','10:05','No Permit','40','2020-10-13','Paid'),
('TRK1093','Rio','Blue','2020-09-21','Premiere Lot','14:00','Expired Permit','25','2020-10-20','Unpaid')]
mycursor.executemany(insert_stmt, info)
server_con.commit()


print("*Insetion of Data Completed*")

###################################################################################################





