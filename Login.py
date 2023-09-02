#===================Importing Modules
from tkinter import *
from tkinter import messagebox
import mysql.connector as c
from mysql.connector import Error
from Manager import admin
#from Products import product

#===================Root Window
root=Tk()
root.configure(background="white")
root.geometry("1525x790+0+0")
root.state("zoomed")
root.title("Super Store Billing Software")
root.iconbitmap('c:/Python 377/CS Store Billing System/Account.ico')
title=Label(root,bg="black",fg="white", text="Billing Software",bd=12,font=("times new roman", 40,"bold"),pady=2).pack(fill=X,pady=10)

#==================Declaring variables
#======Login Frame
m=StringVar()
m.set("Employee")
#==================Functions

def connect():
    try:
        passwd=passwd_txt.get()
        con=c.connect(host="localhost",user="root",passwd=passwd)
    except:
        messagebox.showerror("Super Store Billing system","Password incorrect")
        passwd_txt.delete(0,END)
    if con.is_connected():
        if m.get()=="Manager":
            passwd_txt.delete(0,END)
            messagebox.showinfo("Super Store Billing System","Welcome Manager")
            m.set("Employee")
            admin()
        elif m.get()=="Employee":
            messagebox.showinfo("Super Store Billing System","Welcome Employee")
            passwd_txt.delete(0,END)
            import Final

#===================Login
login_lbl=Label(root,bg="white",text="Login Page",font=("times new roman",30,"bold")).pack(fill=X,pady=10)
welcome_lbl=Label(root,bg="white",text="Welcome to Super Store Billing System!",font=("arial",20)).place(x=550,y=225)

passwd_lbl=Label(root,bg="white",text="Enter the password :",font=("arial",15),pady=5,padx=5)
passwd_lbl.place(x=400,y=330)
passwd_txt=Entry(root,show="*",bg="white",width=50,borderwidth=5,font=("arial",15))
passwd_txt.place(x=600,y=330)
passwd=passwd_txt.get()

mode_lbl=Label(root,bg="white",text="Please select your designation :",font=("arial",15),pady=5,padx=5)
mode_lbl.place(x=400,y=400)

mode_om=OptionMenu(root,m,"Employee","Manager")
mode_om.place(x=800,y=400)

enter_btn=Button(root,command=connect,text="ENTER",width=10,font=("arial",15,"bold"),bg="grey",fg="white").place(x=900,y=470)

root.mainloop()
