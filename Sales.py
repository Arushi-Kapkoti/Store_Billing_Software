#===================Importing Modules
from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector as c
from mysql.connector import Error
from PIL import ImageTk,Image
import os
 
#===================top Window
#Creating a new window for sales details
ts=Toplevel()
ts.configure(background="white")
ts.geometry("1300x750+0+0")
#t.state("zoomed")
ts.title("Super Store Billing Software")
ts.iconbitmap('c:/Python 377/CS Store Billing System/Account.ico')
title=Label(ts,bg="black",fg="white", text="Billing Software",bd=12,font=("times new roman", 40,"bold"),pady=2).pack(fill=X,pady=10)
#Connecting to the database
con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
cursor=con.cursor()
#===================Variables
bill_list=[]
var_invoice=StringVar()
#====================Functions
def show():
    bill_list[:]
    sale_list.delete(0,END)
    for i in os.listdir("bill"):
        if i.split(".")[-1]=="txt":
            sale_list.insert(END,i)
            bill_list.append(i.split(".")[0])



def get_data(ev):
    index_=sale_list.curselection()
    file_name=sale_list.get(index_)
    bill_area.delete("1.0",END)
    fp=open(f"bill/{file_name}", "r")
    for i in fp:
        bill_area.insert(END,i)
    fp.close()


def search():
    if var_invoice.get()=="":
        messagebox.showerror("Error","Invoice no. required", parent=ts)
    else:
        if var_invoice.get() in bill_list:
            fp=open(f"bill/{var_invoice.get()}.txt", "r")
            bill_area.delete("1.0", END)
            for i in fp:
                bill_area.insert(END,i)
            fp.close()

        else:
            messagebox.showerror("Error","Invalid Invoice no.", parent=ts)


def clear():
    show()
    bill_area.delete("1.0",END)


#=============================


#title
title=Label(ts,bg="black",fg="white", text="View Customer Bills",bd=12,font=("times new roman", 25,"bold"),pady=2).pack(fill=X,pady=10)

lbl_invoice=Label(ts, text="Invoice Number" , font=("times new roman",15), bg="white").place(x=50,y=200)
txt_invoice=Entry(ts, textvariable=var_invoice , font=("times new roman",15), bg="white").place(x=160,y=250,height=28)

btn_search=Button(ts, text="Search", command=search , font=("times new roman",15,'bold'), bg="black", fg="white",cursor="hand2").place(x=400,y=250, height=28)
btn_search=Button(ts, text="Clear" ,command=clear, font=("times new roman",15,'bold'), bg="black",fg="white",cursor="hand2").place(x=550,y=250, height=28)


#bill list
sales_Frame=Frame(ts, bd=3, relief=RIDGE)
sales_Frame.place(x=50,y=300,width=200,height=400)
scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
sale_list=Listbox(sales_Frame,font=("goudy old style", 15), bg="white",yscrollcommand=scrolly.set)
scrolly.pack(side=RIGHT, fill=Y)
scrolly.config(command=sale_list.yview)
sale_list.pack(fill=BOTH, expand=1)
sale_list.bind("<ButtonRelease-1>",get_data)

#bill area
bill_Frame=Frame(ts, bd=3, relief=RIDGE)
bill_Frame.place(x=280,y=300,width=420,height=400)

title2=Label(bill_Frame,bg="black",fg="white", text="Customer Bill Area",bd=12,font=("times new roman", 20,"bold"),pady=2).pack(fill=X)


scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
bill_area=Text(bill_Frame, bg="white",yscrollcommand=scrolly2.set)
scrolly2.pack(side=RIGHT, fill=Y)
scrolly2.config(command=bill_area.yview)
bill_area.pack(fill=BOTH, expand=1)

#image

bill_photo=ImageTk.PhotoImage(Image.open("cat.jpg"))

lbl_image=Label(ts,image=bill_photo,bd=0)
lbl_image.place(x=850,y=350)

show()



    
    

            
            
    
    

