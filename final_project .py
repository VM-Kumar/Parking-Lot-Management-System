# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:40:18 2020

@author: venkatesh
"""
import mysql.connector as mysql
import sys
import datetime
from dateutil.relativedelta import relativedelta
from datetime import *

#Establishing Connection
try : 
    con = mysql.connect(
        host= "localhost",
        user= "root",
        passwd= "1186",
        database = "project"
        )   
except mysql.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
#Creating Cursor
mycursor = con.cursor()

############################### ALL THE FUNCTIONS ##################################
def AddLot(name,address,n_spaces,start_n,zone):
     
    insert_stmt1 = f"INSERT INTO p_lots(name,address,zone) VALUES('{name}','{address}','{zone}')"
    mycursor.execute(insert_stmt1)
    con.commit()
    
    for i in range(start_n,start_n+n_spaces):
        insert_stmt2 = f"INSERT INTO spaces(name,sid,space_type) VALUES('{name}',{i},'R')"
        mycursor.execute(insert_stmt2)
        con.commit()

def AssignZoneToLot(name,zones):
    dic = {'A':1,'B':1,'C':1,'D':1,'AS':2,'BS':2,'CS':2,'DS':2,'V':3 }
    individual_zone= zones.split("/")
    
    for zone in individual_zone:
        if zone not in dic:
            print(f"You have entered Invalid Zones :{zone}")
            return zone
    
    update_stmt = f"UPDATE p_lots SET zone = '{zones}' WHERE name = '{name}'"
    mycursor.execute(update_stmt)
    con.commit()
   

def AssignTypeToSpace(name,start_n,end_n,p_type):
    
    dic = {'R':0,'V':1,'E':2,'H':3}
    if p_type not in dic:
        print(f"You have entered an Invalid space type : {p_type} ")
        return p_type
    
    for i in range(start_n,end_n+1):
        update_stmt =  f"UPDATE spaces SET space_type = '{p_type}' WHERE name = '{name}' AND sid = {i}"
        mycursor.execute(update_stmt)
        con.commit()

def AddVehicle(license_no,manufacturer,model,year,color):
    try:
        stmt = f"INSERT INTO vehicle_info(license_no,manufacturer,model,year,color) VALUES('{license_no}','{manufacturer}','{model}','{year}','{color}')"
        mycursor.execute(stmt)
        con.commit()
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
    con.commit()
    
    AddVehicle(license_no, manufacturer, model, year, color)
       


def GetVisitorPermit (UNIQUE_PERMIT_ID,LICENSE_NO,START_DATE,START_TIME,DURATION,LOT,SPACE_TYPE,SPACE_NO,manufacturer, model, year, color):
    insert_stmt = "INSERT INTO VISITOR_PERMITS(UNIQUE_PERMIT_ID ,LICENSE_NO,START_DATE,EXPIRATION_DATE,START_TIME,DURATION,EXPIRATION_TIME,LOT,SPACE_TYPE,SPACE_NO) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    D=START_DATE.split("-")
    T=START_TIME.split(":")
    End=datetime(int(D[0]),int(D[1]),int(D[2]),int(T[0]),int(T[1]))+timedelta(hours=int(DURATION))
    EXPIRATION_DATE=End.strftime("%Y-%m-%d")
    EXPIRATION_TIME=End.strftime("%H:%M")
    
    info=(UNIQUE_PERMIT_ID,LICENSE_NO,START_DATE,EXPIRATION_DATE,START_TIME,DURATION,EXPIRATION_TIME,LOT,SPACE_TYPE,SPACE_NO)
    mycursor.execute(insert_stmt,info)
    con.commit()
    
    AddVehicle(LICENSE_NO, manufacturer, model, year, color)



def IssueCitation(LICENSE_NO,MODEL,COLOR,ISSUE_DATE,LOT,TIME,VIOLATION_CATEGORY,FEE,DUE_DATE):
    Insert_Into_Citation="INSERT INTO CITATIONS(LICENSE_NO,MODEL,COLOR,ISSUE_DATE,LOT,TIME,VIOLATION_CATEGORY,FEE,DUE_DATE) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    info=(LICENSE_NO,MODEL,COLOR,ISSUE_DATE,LOT,TIME,VIOLATION_CATEGORY,FEE,DUE_DATE)
    mycursor.execute(Insert_Into_Citation, info)
    con.commit()
    
    

#GetVisitorPermit('20V0025B','TRK1093', '4' ,'Premiere Lot','Regular','200')



# for visitor permit
def ExitLot(UNIQUE_PERMIT_ID):
    
    Obtain_date_time='''SELECT EXPIRATION_DATE,EXPIRATION_TIME FROM VISITOR_PERMITS 
                  WHERE UNIQUE_PERMIT_ID=\'{a}\''''.format(a=UNIQUE_PERMIT_ID)
    Delete_permit='''DELETE FROM VISITOR_PERMITS
                      WHERE UNIQUE_PERMIT_ID=\'{a}\''''.format(a=UNIQUE_PERMIT_ID) 
    Data_from_permits='''SELECT P.LICENSE_NO,V.MODEL,V.COLOR,P.LOT
                          FROM VEHICLE_INFO V, VISITOR_PERMITS P 
                          WHERE P.LICENSE_NO=V.LICENSE_NO AND P.UNIQUE_PERMIT_ID=\'{a}\''''.format(a=UNIQUE_PERMIT_ID)   
    
    mycursor.execute(Obtain_date_time)
    t=mycursor.fetchall()
    #print('hello')
    #print(t)
    D=t[0][0].strftime("%Y-%m-%d").split("-")
    T=str(t[0][1]).split(":")
        
    given_time=datetime(int(D[0]),int(D[1]),int(D[2]),int(T[0]),int(T[1]),int(T[2]))
    exit_time=datetime.now()
  
    
             
    if given_time<exit_time:
        mycursor.execute(Data_from_permits)
        t=mycursor.fetchall()
        t=t[0]
        print(t)
        A=t[0]
        B=t[1]
        C=t[2]
        D=datetime.now().strftime("%Y-%m-%d")
        E=t[3]
        F=datetime.now().strftime("%H:%M")
        G='Expired Permit'
        H='25'
        I=datetime.now()+timedelta(days=30)
        I=I.strftime("%Y-%m-%d")
        J='Unpaid'
        IssueCitation(A,B,C,D,E,F,G,H,I,J)
        mycursor.execute(Delete_permit)
        con.commit()
        print('citation issued for expired permit')

    mycursor.execute(Delete_permit)
    con.commit()
    print('Permit deallocated and Space is Free')
    
#ExitLot('20V0021L')
        
        
def ChangeVehicleList(UNIQUE_PERMIT_ID,LICENSE_NO,UNIV_ID,AddORDelete):
	Get_count="SELECT COUNT(*) FROM NON_VISITOR_PERMITS WHERE UNIV_ID={a}".format(a=UNIV_ID)
	Get_zone="SELECT ZONE_ID FROM NON_VISITOR_PERMITS WHERE UNIV_ID={a}".format(a=UNIV_ID)
	Get_date_time="SELECT EXPIRATION_DATE,EXPIRATION_TIME FROM NON_VISITOR_PERMITS WHERE LICENSE_NO=\'{a}\'".format(a=LICENSE_NO)
	insert_statement = "INSERT INTO NON_VISITOR_PERMITS(UNIQUE_PERMIT_ID ,CAR_COUNT,ZONE_ID,LICENSE_NO,START_DATE,EXPIRATION_DATE,START_TIME,EXPIRATION_TIME,SPACE_TYPE,UNIV_ID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	delete_statement="DELETE FROM NON_VISITOR_PERMITS WHERE UNIV_ID=\'{a}\' AND LICENSE_NO=\'{b}\'".format(a=UNIV_ID,b=LICENSE_NO)
	
	Data_from_permits='''SELECT P.LICENSE_NO,V.MODEL,V.COLOR,P.LOT FROM VEHICLE_INFO V, VISITOR_PERMITS P WHERE P.LICENSE_NO=V.LICENSE_NO AND P.UNIQUE_PERMIT_ID=\'{a}\''''.format(a=UNIQUE_PERMIT_ID)
	Delete_permit='''DELETE FROM VISITOR_PERMITS
                      WHERE UNIQUE_PERMIT_ID=\'{a}\''''.format(a=UNIQUE_PERMIT_ID)
	mycursor.execute(Get_zone)
	c=mycursor.fetchall()
	dic = {'A':1,'B':1,'C':1,'D':1,'AS':2,'BS':2,'CS':2,'DS':2, None:3 }
	c=c[0]
	status=dic[c[0]]
	mycursor.execute(Get_count)
	c=mycursor.fetchall()
	c=c[0]
	if AddORDelete=='Add':
		if (c[0]>=2 and status==1) or (c[0]>=1 and status==2):
			print('permit cannot be issued,vehicles exceeded')
		else:
			print('Enter comma seperated list of Permit details :\n UNIQUE_PERMIT_ID ,CAR_COUNT,ZONE_ID,LICENSE_NO,START_DATE,EXPIRATION_DATE,START_TIME,EXPIRATION_TIME,SPACE_TYPE,UNIV_ID')
			s=input()
			#print(s)
			s=s.split(",")
			#print(s)
			mycursor.execute(insert_statement,tuple(s))
			
			print("Enter the corresponding vehicle details as a comma separated list:\nLicense number,manufacturer,model,year,color")
			s=input()
			s=s.split(",")
			AddVehicle(	s[0],s[1],s[2],s[3],s[4])
			con.commit()
	else:
		mycursor.execute(Get_date_time)
		t=mycursor.fetchall()
		D=t[0][0].strftime("%Y-%m-%d").split("-")
		T=str(t[0][1]).split(":")
		given_time=datetime(int(D[0]),int(D[1]),int(D[2]),int(T[0]),int(T[1]),int(T[2]))
		exit_time=datetime.now()
        
		if(exit_time<given_time):
			mycursor.execute(delete_statement)
			con.commit()
		else:
			mycursor.execute(Data_from_permits)
			t=mycursor.fetchall()
			t=t[0]
			A=t[0]
			B=t[1]
			C=t[2]
			D=datetime.now().strftime("%Y-%m-%d")
			E='NIL'
			F=datetime.now()+timedelta(days=30)
			F=F.strftime("%Y-%m-%d")
			G='Expired Permit'
			H='25'
			I=datetime.now().strftime("%H:%M")
			J='Unpaid'
			IssueCitation(A,B,C,D,E,F,G,H,I,J)
			mycursor.execute(Delete_permit)
			con.commit()
			print('Permit deallocated and Space is Free...citation issued for expired permit')
            
#ChangeVehicleList('20CS001C','UGB9020','1006003','Del')
    
 
       
def PayCitation():
    Alter_statement='''UPDATE CITATIONS 
                        SET STATUS='Paid'
                        WHERE LICENSE_NO=\'{a}\''''
    
    print("enter Vehicle License_Number")
    n=input()
    mycursor.execute(Alter_statement.format(a=n))
    con.commit()
    
#PayCitation()

def CheckNVValidParking(Given_date,Given_time, Permit_number):
    check_statement='''SELECT COUNT(*)  FROM NON_VISITOR_PERMITS 
                        WHERE UNIQUE_PERMIT_ID=\'{a}\''''.format(a=Permit_number)
    get_date_time='''SELECT EXPIRATION_DATE,EXPIRATION_TIME  FROM NON_VISITOR_PERMITS 
                        WHERE UNIQUE_PERMIT_ID=\'{a}\''''.format(a=Permit_number)
    
    get_assigned_zone= f"SELECT zone_id FROM non_visitor_permits WHERE unique_permit_id = '{Permit_number}'"    
    dic = {'A':1,'B':1,'C':1,'D':1,'AS':2,'BS':2,'CS':2,'DS':2,'V':3 }
    
    mycursor.execute(check_statement)
    permit_check=mycursor.fetchall()
    
    if permit_check[0][0]==0:
        print('No Permit')
        
    else:
        mycursor.execute(get_date_time)
        t=mycursor.fetchall()
        mycursor.execute(get_date_time)
        t=mycursor.fetchall()
        D=t[0][0].strftime("%Y-%m-%d").split("-")
        T=str(t[0][1]).split(":")
        permitted_time=datetime(int(D[0]),int(D[1]),int(D[2]),int(T[0]),int(T[1]),int(T[2]))
        
        CD=Given_date.split("-")
        CT=Given_time.split(":")
        given_time=datetime(int(CD[0]),int(CD[1]),int(CD[2]),int(CT[0]),int(CT[1]))
        
        if given_time>permitted_time:
            print('EXPIRED Permit')
        else:
            print('VALID Permit')
            
#CheckNVValidParking('2020-10-21','09:00','20A0052A')
            
def CheckVValidParking (CurrentTime, Date,Space_number, Lot, License_number):
    
    nopermit_check='''SELECT COUNT(*)  FROM VISITOR_PERMITS 
                        WHERE LICENSE_NO=\'{a}\' '''.format(a=License_number)
    
    check_statement='''SELECT COUNT(*)  FROM VISITOR_PERMITS 
                        WHERE LICENSE_NO=\'{a}\' AND SPACE_NO=\'{b}\' AND LOT=\'{c}\' '''.format(a=License_number,b=Space_number,c=Lot)
    get_date_time='''SELECT EXPIRATION_DATE,EXPIRATION_TIME  FROM VISITOR_PERMITS 
                        WHERE LICENSE_NO=\'{a}\' AND SPACE_NO=\'{b}\' AND LOT=\'{c}\' '''.format(a=License_number,b=Space_number,c=Lot)
    
    
    mycursor.execute(nopermit_check)
    t=mycursor.fetchall()
    t=t[0][0]
        
    if t==0:
        print('No Permit')
        return 0
    
  
    mycursor.execute(check_statement)
    waste = mycursor.fetchall()
    waste = waste[0][0]
    
    if waste==0:
        print('Invalid Permit')
        return 0
    
   
    mycursor.execute(get_date_time)  
    t=mycursor.fetchall()
    D=t[0][0].strftime("%Y-%m-%d").split("-")
    T=str(t[0][1]).split(":")
    permitted_time=datetime(int(D[0]),int(D[1]),int(D[2]),int(T[0]),int(T[1]),int(T[2]))
    
    CD=Date.split("-")
    CT=CurrentTime.split(":")
    given_time=datetime(int(CD[0]),int(CD[1]),int(CD[2]),int(CT[0]),int(CT[1]))
  
    
    if given_time>permitted_time:
        print('EXPIRED Permit')
    else:
        print('VALID Permit')




#CheckNVValidParking('2022-10-21','09:00','20A0052A','KTP2003')

################################## FINAL MENU ######################################


def Visitor_Functions():
    print("Choose Action to perform:\n1.Get a visitor Permit\n2.Exit Parking Lot\n3.Pay Citation Fee")
    a=input()
    if a=='1':
        print('''Enter the following values in order as a comma separated list:
                          \n'UNIQUE_PERMIT_ID,LICENSE_NO,START_DATE,START_TIME,DURATION,LOT,SPACE_TYPE,SPACE_NO,manufacturer, model, year, color''')
        s=input()
        s=s.split(",")
        GetVisitorPermit(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11]) 
                
    elif a=='2':
        print('Enter your Permit ID')
        s=input()
        ExitLot(s)
                
    elif a=='3':            
        PayCitation()
        
    else:
        print('wrong option')
            
        

def StudentEmployee_Functions():
    
    print("Choose Action to perform:\n1.Get a Permit\n2.Change Permit Details(add/remove) \n3.Pay Citation Fee")
    a=input()
    if a=='1':
        print('''Enter the following values in order as a comma separated list:
                          \nunique_permit_id,zone_id,license_no,start_date,space_type,univ_id,manufacturer,model,year,color''')
        s=input()
        s=s.split(",")
        IssuePermit(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9])
    elif a=='2':
        print('Enter Permit_ID,License number,university id .....as a comma seperated list ')
        s=input()
        s=s.split(",")
        print('Do you want to Add or delete permit?(Add/Delete)')
        d=input()
        ChangeVehicleList(s[0],s[1],s[2],d)
        #ChangeVehicleList(UNIQUE_PERMIT_ID,LICENSE_NO,UNIV_ID,AddORDelete)
                            
    elif a=='3':
        PayCitation()
    else:
        print('wrong option')
            
           

def Administrator_Functions():
    print('''Choose Action to perform:
       \n1.Add new Lots
       \n2.Assign zones to lots 
       \n3.Assign types to spaces
       \n4.Issue non visitor permit
       \n5.Issue a visitor Permit
       \n6.Issue a citation
       \n7.Remove a visitor permit
       \n8.Alter non visitor permit data
       \n9.Check if Non Visitor parking data is valid
       \n10.Check if Visitor parking data is valid
       ''')
   
    a=input()
    if a=='1':
        print('''Enter the following lot details as a comma separated list
          \nLot name, Lot Address, Number of spaces, start index of spaces, list of zones''') 
        s=input()
        s=s.split(",")
        
        AddLot(s[0],s[1],int(s[2]),int(s[3]),s[4])
    
    elif a=='2':
        print("Enter the parking Lot name,Zone designation as a comma separated list")
        s=input()
        s=s.split(",")
        AssignZoneToLot(s[0],s[1])
    
    elif a=='3':
        print('''Enter the following details as a comma separated list:
          \nname of parking lot name, start index, end index, corresponding permit type''') 
        s=input()
        s=s.split(",")
        AssignTypeToSpace(s[0],int(s[1]),int(s[2]),s[3])
       
    elif a=='4':
        print('''Enter the following values in order as a comma separated list:
              \nunique_permit_id,zone_id,license_no,start_date,space_type,univ_id,manufacturer,model,year,color''')
        s=input()
        s=s.split(",")
        IssuePermit(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9])
    
    elif a=='5':
        print('''Enter the following values in order as a comma separated list:
          \n'UNIQUE_PERMIT_ID,LICENSE_NO,START_DATE,START_TIME,DURATION,LOT,SPACE_TYPE,SPACE_NO,manufacturer, model, year, color''')
        s=input()
        s=s.split(",")
        GetVisitorPermit(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11]) 
       
    elif a=='6':   
        print("Enter the following details as a comma separated list:\nLICENSE_NO,MODEL,COLOR,ISSUE_DATE,LOT,TIME,VIOLATION_CATEGORY,FEE,DUE_DATE")
        s=input()
        s=s.split(",")
        IssueCitation(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])
    elif a=='7':
        print('Enter the Permit ID')
        s=input()
        ExitLot(s)
    elif a=='8':
        print('Enter Permit_ID,License number,university id .....as a comma seperated list ')
        s=input()
        s=s.split(",")
        print('Do you want to Add or delete permit?(Add/Delete)')
        d=input()
        ChangeVehicleList(s[0],s[1],s[2],d)
    
    elif a=='9':
        print('''Enter the following details as a comma separated list:
          \nCurrent Date,Current Time,Permit Number''')
        s=input()
        s=s.split(",")
        CheckNVValidParking(s[0],s[1],s[2])
    
    elif a=='10':
        print("Enter the following as a comma separated list\nCurrentTime,Current Date,Space_number, Lot name,Vehicle License number")
        s=input()
        s=s.split(",")
        CheckVValidParking (s[0],s[1],s[2],s[3],s[4])
    else:  
        default: print('wrong option')

  
     
                       


print("choose user: \n1.Visitor \n2.Student/Employee \n3.Administrator")
a=input()
if a=='1':
    Visitor_Functions()
elif a=='2':            
    StudentEmployee_Functions()
elif a=='3':          
    Administrator_Functions()
else:         
    print('wrong option');
            



        
        

        
        
        
    
        
    
    

    
    
    
      

      
      

    
                        
