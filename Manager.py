#===================Importing Modules
from tkinter import *
from tkinter import messagebox
import mysql.connector as c
from mysql.connector import Error
from PIL import ImageTk,Image


#===================top Window
def admin():
    top=Toplevel()
    top.configure(background="white")
    top.geometry("1525x790+0+0")
    top.state("zoomed")
    top.title("Super Store Billing Software")
    top.iconbitmap('c:/Python 377/CS Store Billing System/Account.ico')
    title=Label(top,bg="black",fg="white", text="Billing Software",bd=12,font=("times new roman", 40,"bold"),pady=2).pack(fill=X,pady=10)

    #=================Connecting To MySQL
    con=c.connect(host="localhost",user="root",passwd="11235813")
    cursor=con.cursor()
    cursor.execute("show databases;")

    #creating a database dynamically (creates a new database "Store_Billing_System. If it already exists, then connects to the already existing database)
    try:
        cursor.execute("create database Store_Billing_System;")
    except Error:
        con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
        if con.is_connected():
            pass
        else:
            messagebox.showerror("Super Store Billing system","Error opening database.")

    #creating a table dynamically (creates a new table "stock". If it already exists, then it shows a message)
    con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
    cursor=con.cursor()
    try:
        cursor.execute("create table stock(pcode int primary key, pname varchar(30), quantity int, price int,status varchar(30));")
        con.commit()
    except Error:
        pass
    #======================Functions
    def back():
        top.destroy()

    def sales_details():
        import Sales
    
    def product_details():
        import Products

    #======================Manager user window
    manager_lbl=Label(top,bg="white",text="Manager",font=("times new roman",30,"bold")).pack(fill=X,pady=10)

    user_img=ImageTk.PhotoImage(Image.open("user.jpg"))
    user_lbl=Label(top,image=user_img).pack()

    welcome_lbl=Label(top,bg="white",text="What would you like to do today?",font=("arial",20)).place(x=550,y=425)

    product_btn=Button(top,command=product_details,text="Product Details",width=15,font=("arial",15,"bold"),bg="grey",fg="white").place(x=550,y=525)
    sales_btn=Button(top,command=sales_details,text="Sales Details",width=15,font=("arial",15,"bold"),bg="grey",fg="white").place(x=770,y=525)

    back_button=Button(top,text="Back",command=back,width=15,font=("arial",15,"bold"),bg="grey",fg="white").place(x=670,y=630)

    top.mainloop()
