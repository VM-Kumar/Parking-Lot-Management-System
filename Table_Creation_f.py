# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 17:07:25 2020

@author: venkatesh
"""
import mysql.connector as mysql
import sys
import datetime
from datetime import *


host = "localhost"
user = "root"
passwd = "abcd1234"

#Establishes connection to the server and creates a database called "project".
try : 
    server_con = mysql.connect(
        host= host,
        user= user,
        passwd= passwd,
         )
    print("Connection to server Established")
    
except mysql.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))

server_cursor = server_con.cursor()
server_cursor.execute("CREATE DATABASE project")





#Establishes a connection to the Database "project"

try : 
    con = mysql.connect(
        host= host,
        user= user,
        passwd= passwd,
        database = "project"
         )
    print("Connection to Database Established")
    
except mysql.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))

mycursor = con.cursor()


############################### TABLE CREATION ##################################

create_p_lots_table='''CREATE TABLE p_lots(
	name VARCHAR(30) NOT NULL,
	address VARCHAR(50),
    zone VARCHAR(25),
    PRIMARY KEY(name)
    );'''

create_spaces_table='''CREATE TABLE spaces(
	sid INT NOT NULL,
    name VARCHAR(30) NOT NULL,
    space_type VARCHAR(5),
    PRIMARY KEY(name,sid),
    FOREIGN KEY (name) REFERENCES p_lots(name)
    ON DELETE CASCADE
);'''


create_non_visitor_table='''CREATE TABLE NON_VISITOR_PERMITS (
    UNIQUE_PERMIT_ID VARCHAR(8) NOT NULL,
    CAR_COUNT INT default 1,
    ZONE_ID VARCHAR(2),
    LICENSE_NO VARCHAR(10),
    START_DATE DATE,
    EXPIRATION_DATE DATE,
    START_TIME TIME default '00:00',
    EXPIRATION_TIME TIME default '23:59',
    SPACE_TYPE VARCHAR(20),
    UNIV_ID VARCHAR(20),
    PRIMARY KEY(UNIQUE_PERMIT_ID,CAR_COUNT),
    CONSTRAINT check_number_cars CHECK(CAR_COUNT=1 or CAR_COUNT=2),
    CONSTRAINT check_space_type CHECK(SPACE_TYPE='R' or SPACE_TYPE ='V' or SPACE_TYPE='H' or SPACE_TYPE ='E')
    );'''

create_visitor_table='''CREATE TABLE VISITOR_PERMITS (
	UNIQUE_PERMIT_ID VARCHAR(8) NOT NULL,
    LICENSE_NO VARCHAR(10),
    START_DATE DATE,
    EXPIRATION_DATE DATE,
    START_TIME TIME,
    DURATION TIME,
    EXPIRATION_TIME TIME,
    LOT VARCHAR(30),
    SPACE_TYPE VARCHAR(20),
    SPACE_NO INTEGER,
    PRIMARY KEY(UNIQUE_PERMIT_ID),
    CONSTRAINT check_visitor_space CHECK(SPACE_TYPE='R' or SPACE_TYPE ='V' or SPACE_TYPE='H' or SPACE_TYPE ='E'),
    FOREIGN KEY (LOT) REFERENCES p_lots(name)
    );'''

create_vehicle_info_table='''CREATE TABLE VEHICLE_INFO(
    LICENSE_NO VARCHAR(15),
    MANUFACTURER VARCHAR(15),
    MODEL VARCHAR(15),
    YEAR VARCHAR(4),
    COLOR VARCHAR(10),
    PRIMARY KEY(LICENSE_NO) );'''
    
create_table_citations='''CREATE TABLE CITATIONS(
    UNIQUE_CITATION_NUMBER INTEGER(5) AUTO_INCREMENT,
    LICENSE_NO VARCHAR(15),
    MODEL VARCHAR(15), 
    COLOR VARCHAR(10), 
    ISSUE_DATE DATE,
    LOT VARCHAR(15),
    TIME TIME,
    VIOLATION_CATEGORY VARCHAR(25),
    FEE INTEGER(2),
    DUE_DATE DATE, 
    STATUS VARCHAR(6) DEFAULT 'Unpaid',
    PRIMARY KEY(UNIQUE_CITATION_NUMBER),
    CONSTRAINT check_violation_category CHECK(VIOLATION_CATEGORY='Invalid Permit' OR VIOLATION_CATEGORY='Expired Permit' OR VIOLATION_CATEGORY='No Permit'),
    CONSTRAINT check_fee CHECK(FEE=20 OR FEE=25 OR FEE=40)
);'''

mycursor.execute(create_non_visitor_table)
mycursor.execute(create_p_lots_table)
mycursor.execute(create_visitor_table)
mycursor.execute(create_vehicle_info_table)
mycursor.execute(create_table_citations)
mycursor.execute("ALTER TABLE CITATIONS AUTO_INCREMENT=10001")
mycursor.execute(create_spaces_table)

print("**ALL Tables Have been Created**")
#######################################################################################