import mysql.connector as mys
import smtplib
import random
systemmail="definetestmail@gmail.com"
server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(systemmail, "sjnk zwwy vugi teoo")

loggeduser = ""  

def verifymail(mailid):
    global systemmail
    subject="Community-D-Services Verfication System"
    message=("Your verification code is")
    code=random.randint(100000,999999)
    text=f"Subject:{subject}\n\n{message,code}"
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(systemmail, "sjnk zwwy vugi teoo")
    server.sendmail(systemmail,mailid,text)
    print("Check your mail for the 6-digit verification code")
    verify=int(input("Enter your 6 digit verification code: "))
    if verify==code:
        return True

def signup():
    global loggeduser  
    print("Welcome to Community-D-Systems")
    mailid = input("Enter your contact mail address (This will be your username): ")
    if verifymail(mailid):
        print("Successfully Verified")
        name = input("Enter your name: ")
        phno = input("Enter your 10 digit contact number: ")
        district = input("Enter your district: ")
        blood = input("Enter your blood group: ")
        aadhar = input("Enter your 16 digit Aadhar number: ")
        passw = input("Enter a password: ")
        vol = input("Would you like to register as a volunteer? (y/n): ").lower()
        insert_query = "INSERT INTO volunteers VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (name, phno, mailid, district, blood, aadhar, vol, passw)
        cursor.execute(insert_query, data)
        mycon.commit()
        loggeduser = mailid 
        login()
    else:
        print("E-mail verification failed")

def login():
    global loggeduser  
    userid = input("Enter your userid: ")
    password = input("Enter your password: ")
    query = "SELECT * FROM volunteers WHERE mailid = %s AND passw = %s"
    cursor.execute(query, (userid, password))
    result = cursor.fetchone()
    if result:
        print("Successful Login")
        loggeduser = userid  
    helpp=input("Are you seeking for help from our volunteers? (y/s)")
    helpp=helpp.lower()
    if helpp=='y':
        help()

def help():
    global loggeduser
    global systemmail
    global server
    if loggeduser:
        
        cursor.execute("SELECT name,district,phno FROM volunteers WHERE mailid = %s", (loggeduser,))
        result = cursor.fetchone()
        if result:
            district = result[1]
            name=result[0]
            phno=result[2]
            cursor.execute("SELECT mailid FROM volunteers WHERE district = %s", (district,))
            mails = cursor.fetchall()
            list_mail = [mail[0] for mail in mails]
            subject="Emergency Support Request"
            location=input("Enter your exact location: ")
            message=(name,"from",location,"is requesting your help in an emergency situation.\nPlease Connect with your friends and contact",name,"via Telecom:",phno,"and e-mail:",loggeduser,"for any further details from their side")
            text=f"Subject:{subject}\n\n{message}"
            for i in list_mail:
                server.sendmail(systemmail,i,text)
        else:
            print("User not found or district not specified.")
    else:
        print("Please log in first.")


mycon = mys.connect(host="localhost", user="root", passwd="Root@123", database="data")

while True:
    if mycon.is_connected():
        cursor = mycon.cursor()
        choice=int(input("1. Login\n2. Signup\n3. Exit"))
        if choice==1:
            login()
        elif choice==2:
            signup()
        elif choice==3:
            break
    cursor.close()
    mycon.close()
else:
    print("Database connection failed.")
