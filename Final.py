#===================Importing Modules
from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector as c
from mysql.connector import Error
from PIL import ImageTk,Image
import time
import os
import tempfile
#===================top Window

#Creating a new window for billing
t1=Toplevel()
t1.configure(background="white")
t1.geometry("1400x700+0+0")
#t1.state("zoomed")
t1.title("Super Store Billing Software")
t1.iconbitmap('c:/Python 377/CS Store Billing System/Account.ico')
title=Label(t1,bg="black",fg="white", text="Billing Software",bd=12,font=("times new roman", 40,"bold"),pady=2).pack(fill=X,pady=10)
#Connecting to the database
con=c.connect(host="localhost",user="root",passwd="11235813", database="store_billing_system")
cursor=con.cursor()
#Variables
cart_list=[]
chk_print=0
#================Functions
def show():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="store_billing_system")
    cursor=con.cursor()
    try:
        cursor.execute("select* from stock where status='Active';")
        rows=cursor.fetchall()
        product_table.delete(*product_table.get_children())
        for a in rows:
            product_table.insert('',END,values=a)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to :{str(ex)}")
        

def search():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
    cursor=con.cursor()
    global search_txt
    try:
        if var_search.get()=='':
            messagebox.showerror("Error","Search input is required",parent=t)
        else:
            cursor.execute("select * from stock where pname like '"+var_search.get()+"%' and status='Active';")
            rows=cursor.fetchall()
            if len(rows)!=0:
                product_table.delete(*product_table.get_children())
                for a in rows:
                    product_table.insert('',END,values=a)
            else:
                 messagebox.showerror("Error","No record is found",parent=t1)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to :{str(ex)}")


def get_data(ev):
    f=product_table.focus()
    content=(product_table.item(f))
    row=content['values']
    var_pcode.set(row[0])
    var_pname.set(row[1])
    var_price.set(row[3])
    lbl_inStock.config(text="In Stock {}".format(str(row[2])))
    var_stock.set(row[2])
    var_qty.set('1')

def get_data_cart(ev):
    f=cart_table.focus()
    content=(cart_table.item(f))
    row=content['values']
    var_pcode.set(row[0])
    var_pname.set(row[1])
    var_qty.set(row[2])
    var_price.set(row[3])
    lbl_inStock.config(text="In Stock {}".format(str(row[4])))
    var_stock.set(row[4])   

def add_update_cart():
    if var_pcode.get()=='':
        messagebox.showerror("Error","Please select product from the list",parent=t1)
    elif var_qty.get()=='':
        messagebox.showerror("Error","Please enter quantity of the product",parent=t1)
    elif int(var_qty.get())>int(var_stock.get()):
        messagebox.showerror("Error","Invalid Quantity",parent=t1)
    else:
        price_cal=var_price.get()
        cart_data=[var_pcode.get(),var_pname.get(),var_qty.get(),price_cal,var_stock.get()]
        
        #===============Update_Cart===============
        present='no'
        index_=0
        for row in cart_list:
            if var_pcode.get()==row[0]:
                present='yes'
                break
            index_+=1
        if present=='yes':
            op=messagebox.askyesno("Confirm","\tProduct already present in cart\nDo you want to Update Cart/Remove product from cart list?",parent=t1)
            if op==True:
                if var_qty.get()=="0":
                    cart_list.pop(index_)
                else:
                    cart_list[index_][2]=var_qty.get()#qty
        else:
            cart_list.append(cart_data)
        show_cart()
        bill_updates()

def bill_updates():
    global bill_amnt
    global net_pay
    global discount
    bill_amnt=0
    net_pay=0
    discount=0
    global cartTitle 
    for row in cart_list:
        bill_amnt=bill_amnt+(float(row[3])*int(row[2]))
    discount=(bill_amnt*5)/100
    net_pay=bill_amnt-((bill_amnt*5)/100)
    lbl_amnt.config(text=f"Bill Amount\n(Rs.){str(bill_amnt)}")
    lbl_net_pay.config(text=f"Net Amount\n(Rs.){str(net_pay)}")
    cartTitle.config(text=f"Shopping Cart \t\t\tTotal Products: [{str(len(cart_list))}]")

def show_cart():
    try:
        cart_table.delete(*cart_table.get_children())
        for row in cart_list:
            cart_table.insert('',END,values=row)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=t1)

         
def clear_cart():
    var_pcode.set('')
    var_pname.set('')
    var_price.set('')
    var_qty.set('')
    lbl_inStock.config(text=f" In Stock")
    var_stock.set('')


def bill_top():
    global invoice
    invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
    bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 98725***** , Delhi-125001
{str("="*47)}
 Customer Name: {var_cname.get()}
 Ph no. :{var_contact.get()}
 Bill No. {str(invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
    txt_bill_area.delete('1.0',END)
    txt_bill_area.insert('1.0',bill_top_temp)

def bill_bottom():
    bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{bill_amnt}
 Discount\t\t\t\tRs.{discount}
 Net Pay\t\t\t\tRs.{net_pay}
{str("="*47)}\n
        '''
    txt_bill_area.insert(END,bill_bottom_temp)
    
def bill_middle():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="store_billing_system")
    cursor=con.cursor()
    try:
        for row in cart_list:
            pid=row[0]
            name=row[1]
            qty=row[2]
            qty2=int(row[4])-int(row[2])
            if int(qty)==int(row[4]):
                status="Inactive"
            if int(qty)!=int(row[4]):
                status="Active"
            price=float(row[3])*int(row[2])
            price=str(price)
            txt_bill_area.insert(END,"\n "+name+"\t\t\t"+str(qty)+"\tRs."+str(price))
            #======Updating stock table
            cursor.execute("update stock set quantity={},status='{}' where pcode={};".format(qty2,status,pid))
            con.commit()
        show()
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=t1)


def generate_bill():
    if var_cname.get()=='' or var_contact.get()=='':
        messagebox.showerror("Error",f"Customer Details are required",parent=t1)
    elif len(cart_list)== 0:
        messagebox.showerror("Error",f"Please add products to cart",parent=t1)
    else:
        bill_top()
        bill_middle()
        bill_bottom()
        global invoice
        fp=open(f'bill/{str(invoice)}.txt','w')
        fp.write(txt_bill_area.get('1.0',END))
        fp.close()
        messagebox.showinfo('Saved',"Bill has been saved",parent=t1)
        global chk_print
        chk_print=1

                
def clear_all():
    global txt_bill_area
    del cart_list[:]
    var_cname.set('')
    var_contact.set('')
    txt_bill_area.delete('1.0',END)
    cartTitle.config(text=f"Cart \t Total Product: [0]")
    var_search.set('')
    clear_cart()
    show()
    show_cart()

def print_bill():
    global chk_print
    if chk_print==1:
        messagebox.showinfo('Print Bill',"Please wait while the bill is generated",parent=t1)
        new_file=tempfile.mktemp('.txt')
        open(new_file,'w').write(txt_bill_area.get('1.0',END))
        os.startfile(new_file,'print')
    else:
        messagebox.showerror('Print Bill',"Please generate bill to print the receipt",parent=t1)
    chk_print=0
    
#===Product_Frame===

ProductFrame1=Frame(t1,bd=4, relief=RIDGE, bg="white")
ProductFrame1.place(x=6,y=110,width=410,height=550)

pTitle=Label(ProductFrame1,text="All Products",font=("times new roman",20,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)

#===Product Search Frame==============
var_search=StringVar()

ProductFrame2=Frame(ProductFrame1,bd=2, relief=RIDGE, bg="white")
ProductFrame2.place(x=2,y=42,width=398,height=90)

lbl_search=Label(ProductFrame2,text="Search Product [By Name] ",font=("times new roman" ,16,"bold"),bg="white",fg="black").place(x=2,y=5)

lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman" ,15,"bold"),bg="white",fg="black").place(x=2,y=45)
txt_search=Entry(ProductFrame2,textvariable=var_search,font=("times new roman" ,15),bg="light grey").place(x=128,y=47,width=150,height=22)
btn_search=Button(ProductFrame2,command=search,text="Search",font=("times new roman",15),bg="black",fg="white").place(x=285,y=45,width=100,height=25)
btn_show_all=Button(ProductFrame2,text="Show All",command=show,font=("times new roman",15),bg="black",fg="white").place(x=285,y=10,width=100,height=25)

#===Product Details Frame=============
ProductFrame3=Frame(ProductFrame1,bg="white",bd=3,relief=RIDGE)
ProductFrame3.place(x=2,y=140,width=398,height=375)

scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

product_table=ttk.Treeview(ProductFrame3,columns=("pcode","pname","quantity","price",'status'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
scrolly.pack(side=RIGHT,fill=Y)
scrollx.pack(side=BOTTOM,fill=X)
scrolly.config(command=product_table.yview)
scrollx.config(command=product_table.xview)

product_table.heading("pcode",text="Product Code")
product_table.heading("pname",text="Product Name")
product_table.heading("quantity",text="QTY")
product_table.heading("price",text="Price")
product_table.heading("status",text="Status")
product_table["show"]="headings"

product_table.column("pcode",width=85)
product_table.column("pname",width=100)
product_table.column("quantity",width=50)
product_table.column("price",width=60)
product_table.column("status",width=70)

product_table.pack(fill=BOTH,expand=1)

product_table.bind("<ButtonRelease-1>",get_data)
lbl_note=Label(ProductFrame1,text="Note: Enter '0' Quantity to remove product from the cart", font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

show()
#=====CustomerFrame=============

var_cname=StringVar()
var_contact=StringVar()
CustomerFrame=Frame(t1,bd=4, relief=RIDGE, bg="white")
CustomerFrame.place(x=420,y=110,width=530,height=90)

cTitle=Label(CustomerFrame,text="Customer Details",font=("times new roman",15,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)
lbl_cname=Label(CustomerFrame,text="Name",font=("times new roman" ,15),bg="white",fg="black").place(x=5,y=35)
txt_cname=Entry(CustomerFrame,textvariable=var_cname,font=("times new roman" ,13),bg="light grey").place(x=80,y=35,width=180)

lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman" ,15),bg="white",fg="black").place(x=270,y=35)
txt_contact=Entry(CustomerFrame,textvariable=var_contact,font=("times new roman" ,13),bg="light grey").place(x=380,y=35,width=140)

#===ADD Cart Buttons===============

CartFrame=Frame(t1,bg="white",bd=3,relief=RIDGE)
CartFrame.place(x=420,y=190,width=530,height=360)
cartTitle=Label(CartFrame,text="Shopping Cart \t\t\tTotal Products: [0]",font=("times new roman",15,"bold"),bg="light grey",fg="black")
cartTitle.pack(side=TOP,fill=X)

scrolly=Scrollbar(CartFrame,orient=VERTICAL)
scrollx=Scrollbar(CartFrame,orient=HORIZONTAL)

cart_table=ttk.Treeview(CartFrame,columns=("pcode","pname","quantity","price"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
scrolly.pack(side=RIGHT,fill=Y)
scrollx.pack(side=BOTTOM,fill=X)
scrolly.config(command=cart_table.yview)
scrollx.config(command=cart_table.xview)

cart_table.heading("pcode",text="Product Code")
cart_table.heading("pname",text="Product Name")
cart_table.heading("quantity",text="QTY")
cart_table.heading("price",text="Price")
cart_table["show"]="headings"

cart_table.column("pcode",width=85)
cart_table.column("pname",width=170)
cart_table.column("quantity",width=115)
cart_table.column("price",width=150)

cart_table.pack(fill=BOTH,expand=1)

cart_table.bind("<ButtonRelease-1>",get_data_cart)


#===ADD Cart Widgets===================
var_pcode=StringVar()
var_pname=StringVar()
var_price=StringVar()
var_qty=StringVar()
var_stock=StringVar()

Add_CartWidgetsFrame=Frame(t1,bd=2,relief=RIDGE,bg="white")
Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=105)

lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name:", font=("times new roman",15),bg="white").place(x=5,y=5)
txt_p_name=Label(Add_CartWidgetsFrame,textvariable=var_pname, font=("times new roman",15),bg="light grey",state=DISABLED).place(x=5,y=35,width=190,height=24)

lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty:", font=("times new roman",15),bg="white").place(x=230,y=5)
txt_p_price=Label(Add_CartWidgetsFrame,textvariable=var_price, font=("times new roman",15),bg="light grey",state=DISABLED).place(x=230,y=35,width=120,height=22)

lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity:", font=("times new roman",15),bg="white").place(x=390,y=5)
txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=var_qty, font=("times new roman",15),bg="light grey").place(x=390,y=35,width=120,height=22)

lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock:", font=("times new roman",15),bg="white")
lbl_inStock.place(x=5,y=70)


btn_clear_cart=Button(Add_CartWidgetsFrame,command=clear_cart,text="Clear Cart",font=("times new roman",15,"bold"),bg="white").place(x=180,y=70,width=150,height=30)
btn_add_cart=Button(Add_CartWidgetsFrame,text="Add/Update Cart",command=add_update_cart,font=("times new roman",15,"bold"),bg="black",fg="white").place(x=340,y=70,width=180,height=30)

#===================Billing Area===================

BillFrame=Frame(t1,bd=2,relief=RIDGE,bg="white")
BillFrame.place(x=953,y=110,width=410,height=410)

pTitle=Label(BillFrame,text="Customer Bill",font=("times new roman",20,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)
scrolly=Scrollbar(BillFrame,orient=VERTICAL)
scrolly.pack(side=RIGHT,fill=Y)

txt_bill_area=Text(BillFrame,yscrollcommand=scrolly.set)
txt_bill_area.pack(fill=BOTH,expand=1)
scrolly.config(command=txt_bill_area.yview)

#============Billing Buttons=============

BillMenuFrame=Frame(t1,bd=2,relief=RIDGE,bg="white")
BillMenuFrame.place(x=953,y=520,width=410,height=140)

lbl_amnt=Label(BillMenuFrame, text="Bill Amount\n[0]",font=("times new roman",15,"bold"),bg="light grey")
lbl_amnt.place(x=15,y=5,width=120,height=70)

lbl_discount=Label(BillMenuFrame, text="Discount\n[5%]",font=("times new roman",15,"bold"),bg="light grey")
lbl_discount.place(x=160,y=5,width=90,height=70)

lbl_net_pay=Label(BillMenuFrame, text="Net\n Amount\n[0]",font=("times new roman",15,"bold"),bg="light grey")
lbl_net_pay.place(x=270,y=5,width=120,height=70)

btn_print=Button(BillMenuFrame,command=print_bill, text="Print Receipt",font=("times new roman",15,"bold"),bg="black",fg="white")
btn_print.place(x=15,y=80,width=120,height=50)

btn_clear_all=Button(BillMenuFrame,command=clear_all, text="Clear All",font=("times new roman",15,"bold"),bg="black",fg="white")
btn_clear_all.place(x=160,y=80,width=90,height=50)

btn_generate=Button(BillMenuFrame,command=generate_bill, text="Generate\nBill",font=("times new roman",15,"bold"),bg="black",fg="white")
btn_generate.place(x=270,y=80,width=120,height=50)






               
















