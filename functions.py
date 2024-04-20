import mysql.connector as mys
import smtplib
import random
def verifymail(mailid):
    systemmail="definetestmail@gmail.com"
    subject="Community-D-Services Verfication System"
    message=random.randint(1000, 9999)
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email, "sjnk zwwy vugi teoo")



mycon = mys.connect(host="localhost", user="root", passwd="Root@123", database="data")

if mycon.is_connected():
    cursor = mycon.cursor()
    def signup():
        print("Welcome to Community-D-Systems")
        
        name = input("Enter your name: ")
        phno = input("Enter your 10 digit contact number: ")
        mailid = input("Enter your contact mail address(This will be your username): ")

        district = input("Enter your district: ")
        blood = input("Enter your blood group: ")
        aadhar = input("Enter your 16 digit Aadhar number: ")
        passw=input("Enter a password: ")
        vol=input("Would you like to register as a volunteer? (y/n): ")
        if vol=='Y'.lower or 'N'.lower():
            insert_query = "INSERT INTO volunteers VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (name, phno, mailid, district, blood, aadhar, vol, passw)
            cursor.execute(insert_query,data)
            mycon.commit()


    def login():
        userid=input("Enter your userid: ")
        password=input("Enter your password: ")
        query = "SELECT * FROM volunteers WHERE mailid = %s AND passw = %s"
        cursor.execute(query, (userid, password))
        result=cursor.fetchone()
        cursor.close()
        if (result is not None)== True:
            print("Successful Login")

    def volunteer():
        name = input("Enter your name: ")
        phno = input("Enter your 10 digit contact number: ")
        mailid = input("Enter your contact mail address: ")
        district = input("Enter your district: ")
        blood = input("Enter your blood group: ")
        aadhar = input("Enter your 16 digit Aadhar number: ")

        insert_query = "INSERT INTO volunteers VALUES (%s, %s, %s, %s, %s, %s)"
        data = (name, phno, mailid, district, blood, aadhar)

        cursor.execute(insert_query, data)
        mycon.commit()
        print("Volunteer details inserted successfully!")
    
login()
        
