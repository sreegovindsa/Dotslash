import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import mysql.connector as mys
import smtplib
import random

systemmail = "definetestmail@gmail.com"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(systemmail, "sjnk zwwy vugi teoo")

loggeduser = ""  


name_entry = None
phno_entry = None
userid_entry = None
district_entry = None
blood_entry = None
aadhar_entry = None
passw_entry = None
vol_entry = None
login_userid_entry = None
login_passw_entry = None

def verifymail(mailid):
    global systemmail
    subject = "Community-D-Services Verfication System"
    message = "Your verification code is"
    code = random.randint(100000, 999999)
    text = f"Subject:{subject}\n\n{message, code}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(systemmail, "sjnk zwwy vugi teoo")
    server.sendmail(systemmail, mailid, text)
    messagebox.showinfo("Verification", "Check your mail for the 6-digit verification code")
    verify = simpledialog.askinteger("Verification", "Enter your 6 digit verification code: ")
    if verify == code:
        return True

def signup():
    global loggeduser  
    mailid = userid_entry.get()
    if verifymail(mailid):
        messagebox.showinfo("Verification", "Successfully Verified")
        name = name_entry.get()
        phno = phno_entry.get()
        district = district_entry.get()
        blood = blood_entry.get()
        aadhar = aadhar_entry.get()
        passw = passw_entry.get()
        vol = vol_entry.get()
        insert_query = "INSERT INTO volunteers VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (name, phno, mailid, district, blood, aadhar, vol, passw)
        cursor.execute(insert_query, data)
        mycon.commit()
        loggeduser = mailid  
        login()
    else:
        messagebox.showerror("Verification Failed", "E-mail verification failed")

def login():
    global loggeduser  
    userid = login_userid_entry.get()
    password = login_passw_entry.get()
    query = "SELECT * FROM volunteers WHERE mailid = %s AND passw = %s"
    cursor.execute(query, (userid, password))
    result = cursor.fetchone()
    if result:
        loggeduser = userid  
        messagebox.showinfo("Login", "Successful Login")
        helpp = messagebox.askquestion("Help", "Are you seeking for help from our volunteers?")
        if helpp == 'yes':
            help()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def help():
    global loggeduser
    global systemmail
    global server
    if loggeduser:
        
        cursor.execute("SELECT name,district,phno FROM volunteers WHERE mailid = %s", (loggeduser,))
        result = cursor.fetchone()
        if result:
            district = result[1]
            name = result[0]
            phno = result[2]  
            
            cursor.execute("SELECT mailid FROM volunteers WHERE district = %s", (district,))
            mails = cursor.fetchall()
            list_mail = [mail[0] for mail in mails]
            subject = "Emergency Support Request"
            location = simpledialog.askstring("Location", "Enter your exact location:")
            message = (name, "from", location, "is requesting your help in an emergency situation.\nPlease Connect with your friends and contact", name, "via Telecom:", phno, "and e-mail:", loggeduser, "for any further details from their side")
            text = f"Subject:{subject}\n\n{message}"
            for i in list_mail:
                server.sendmail(systemmail, i, text)
        else:
            messagebox.showerror("Error", "User not found or district not specified.")
    else:
        messagebox.showerror("Error", "Please log in first.")

def close_window():
    mycon.close()
    root.destroy()

def open_signup_window():
    global name_entry, phno_entry, userid_entry, district_entry, blood_entry, aadhar_entry, passw_entry, vol_entry
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    
    name_label = ttk.Label(signup_window, text="Name:")
    name_label.pack()
    name_entry = ttk.Entry(signup_window)
    name_entry.pack()

    phno_label = ttk.Label(signup_window, text="Phone Number:")
    phno_label.pack()
    phno_entry = ttk.Entry(signup_window)
    phno_entry.pack()

    userid_label = ttk.Label(signup_window, text="User ID (Email):")
    userid_label.pack()
    userid_entry = ttk.Entry(signup_window)
    userid_entry.pack()

    district_label = ttk.Label(signup_window, text="District:")
    district_label.pack()
    district_entry = ttk.Entry(signup_window)
    district_entry.pack()

    blood_label = ttk.Label(signup_window, text="Blood Group:")
    blood_label.pack()
    blood_entry = ttk.Entry(signup_window)
    blood_entry.pack()

    aadhar_label = ttk.Label(signup_window, text="Aadhar Number:")
    aadhar_label.pack()
    aadhar_entry = ttk.Entry(signup_window)
    aadhar_entry.pack()

    passw_label = ttk.Label(signup_window, text="Password:")
    passw_label.pack()
    passw_entry = ttk.Entry(signup_window, show="*")
    passw_entry.pack()

    vol_label = ttk.Label(signup_window, text="Volunteer (y/n):")
    vol_label.pack()
    vol_entry = ttk.Entry(signup_window)
    vol_entry.pack()

    signup_button = ttk.Button(signup_window, text="Sign Up", command=signup)
    signup_button.pack()

def open_login_window():
    global login_userid_entry, login_passw_entry
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    
    userid_label = ttk.Label(login_window, text="User ID:")
    userid_label.pack()
    login_userid_entry = ttk.Entry(login_window)
    login_userid_entry.pack()

    passw_label = ttk.Label(login_window, text="Password:")
    passw_label.pack()
    login_passw_entry = ttk.Entry(login_window, show="*")
    login_passw_entry.pack()

    login_button = ttk.Button(login_window, text="Login", command=login)
    login_button.pack()


mycon = mys.connect(host="localhost", user="root", passwd="Root@123", database="data")

if mycon.is_connected():
    cursor = mycon.cursor()

    root = tk.Tk()
    root.title("Community-D-Systems")
    root.geometry("300x300")

    
    frame = ttk.Frame(root)
    frame.pack(expand=True)

    
    button_padx = 20
    button_pady = 10

    
    signup_button = ttk.Button(frame, text="Sign Up", command=open_signup_window)
    signup_button.pack(fill="x", padx=button_padx, pady=button_pady)

    login_button = ttk.Button(frame, text="Login", command=open_login_window)
    login_button.pack(fill="x", padx=button_padx, pady=button_pady)

    exit_button = ttk.Button(frame, text="Exit", command=close_window)
    exit_button.pack(fill="x", padx=button_padx, pady=button_pady)

    
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))

    root.mainloop()
else:
    print("Database connection failed.")
