#===================Importing Modules
from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector as c
from mysql.connector import Error
from PIL import ImageTk,Image

#===================top Window
#Creating a new window for product details
t=Toplevel()
t.configure(background="white")
t.geometry("1400x700+0+0")
#t.state("zoomed")
t.title("Super Store Billing Software")
t.iconbitmap('c:/Python 377/CS Store Billing System/Account.ico')
title=Label(t,bg="black",fg="white", text="Billing Software",bd=12,font=("times new roman", 40,"bold"),pady=2).pack(fill=X,pady=10)
#Connecting to the database
con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
cursor=con.cursor()
#=================Defining variables
#Manage Products frame
var_name=StringVar()
var_price=StringVar()
var_qty=StringVar()
var_status=StringVar()
var_pcode=StringVar()
#Search Frame
var_pcode=StringVar()
var_search=StringVar()
var_search_product=StringVar()
#=====================Functions

def show():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
    cursor=con.cursor()
    try:
        cursor.execute("select * from stock")
        rows=cursor.fetchall()
        product_table.delete(*product_table.get_children())
        for a in rows:
            product_table.insert('',END,values=a)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to :{str(ex)}")

def add():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
    cursor=con.cursor()
    try:
        if var_name.get()==''or var_price.get()=='' or var_qty.get()=='':
            messagebox.showerror("Error","Compulsory fields. Please enter respective data to proceed.",parent=t)
        else:
            cursor.execute("select pname from stock;")
            row=cursor.fetchall()
            con.commit()
            flag=True
            for i in row:
                if i[0]==var_name.get():
                    messagebox.showerror("Error","This Product already exists. Try a different product name.",parent=t)
                    name_txt.delete(0,END)
                    price_txt.delete(0,END)
                    qty_txt.delete(0,END)
                    flag=False
                    break
            if flag==True:
                cursor.execute("select max(pcode) from stock;")
                data=cursor.fetchone()
                con.commit()
                if data==(None,):
                    var_pcode=0
                else:
                    var_pcode=str(data[0]+1)
                cursor.execute("insert into stock values({},'{}',{},{},'{}');".format(var_pcode,var_name.get(),var_qty.get(),var_price.get(),var_status.get()))
                con.commit()
                messagebox.showinfo("Success","Product added successfully.",parent=t)
                show()
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to :{str(ex)}")

def get_data(ev):
    f=product_table.focus()
    content=(product_table.item(f))
    row=content['values']
    var_name.set(row[1])
    var_qty.set(row[2])
    var_price.set(row[3])
    var_status.set(row[4])

def update():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
    cursor=con.cursor()
    global product_table
    f=product_table.focus()
    content=product_table.item(f)
    row=content['values']
    name=row[1]
    global var_name
    if var_name.get()==''or var_price.get()=='' or var_qty.get()=='':
        messagebox.showerror("Error","Compulsory fields. Please enter respective data to proceed.",parent=t)
        name_txt.delete(0,END)
        price_txt.delete(0,END)
        qty_txt.delete(0,END)
        return()
    try:
        cursor.execute("select pname,pcode from stock;")
        r=cursor.fetchall()
        pc=''
        for h in r:
            if h[0]==name:
                pc=h[1]
    except:
        messagebox.showerror("Error","Invalid Product.",parent=t)
    else:
       cursor.execute("update stock set pname='{}',quantity={},price={},status='{}' where pcode={};".format(var_name.get(),var_qty.get(),var_price.get(),var_status.get(),pc))
       con.commit()
       messagebox.showinfo("Success","Product details updated successfully.",parent=t)
       show()
    finally:
        name_txt.delete(0,END)
        price_txt.delete(0,END)
        qty_txt.delete(0,END)
        search_txt.delete(0,END)
        var_status.set("Active")

#=====================================================
def delete():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
    cursor=con.cursor()
    if var_name.get()==''or var_price.get()=='' or var_qty.get()=='':
        messagebox.showerror("Error","Compulsory fields. Please enter respective data to proceed.",parent=t)
        name_txt.delete(0,END)
        price_txt.delete(0,END)
        qty_txt.delete(0,END)
        return()
    op=messagebox.askyesno("Confirm","Do you really want to delete this product?",parent=t)
    if op==True:
        try:
            global product_table
            f=product_table.focus()
            content=product_table.item(f)
            row=content['values']
            code=row[0]
            cursor.execute("delete from stock where pcode={};".format(code))
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
        else:
            messagebox.showinfo("Success","Product deleted successfully.",parent=t)
            show()
        finally:
            name_txt.delete(0,END)
            price_txt.delete(0,END)
            qty_txt.delete(0,END)
            search_txt.delete(0,END)
            var_status.set("Active")
    else:
        name_txt.delete(0,END)
        price_txt.delete(0,END)
        qty_txt.delete(0,END)
        search_txt.delete(0,END)
        var_status.set("Active")
#===================================================
def clear():
    var_pcode.set('')
    var_name.set('')
    var_qty.set('')
    var_price.set('')
    var_status.set("Active")
#==================================================
def search():
    con=c.connect(host="localhost",user="root",passwd="11235813", database="Store_Billing_System")
    cursor=con.cursor()
    global search_txt
    try:
        if var_search=="Select":
            messagebox.showerror("Error","Choose an option to search",parent=t)
        elif search_txt.get()=='':
            messagebox.showerror("Error","Search input is required",parent=t)
        elif var_search.get()=="Product Name":
            cursor.execute("select * from stock where pname like '"+search_txt.get()+"%';")
            rows=cursor.fetchall()
            if len(rows)!=0:
                product_table.delete(*product_table.get_children())
                for a in rows:
                    product_table.insert('',END,values=a)
            else:
                 messagebox.showerror("Error","No record is found",parent=t)
        else:
            cursor.execute("select * from stock where pcode like '"+search_txt.get()+"%';")
            rows=cursor.fetchall()
            if len(rows)!=0:
                product_table.delete(*product_table.get_children())
                for a in rows:
                    product_table.insert('',END,values=a)
            else:
                 messagebox.showerror("Error","No record is found",parent=t)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to :{str(ex)}")
#===========================================
def exit():
    t.destroy()
    

#======================Adding Frames and Widgets
#Frame to manage products
F1=Frame(t,bg="white",bd=5,relief=RIDGE)
F1.place(x=10,y=125,width=500,height=515)
title_lbl=Label(F1,text="Manage Product Details",bg="grey",fg="white",font=("arial",20,"bold"),width=30).pack(side=TOP,fill=X)

name_lbl=Label(F1,text="Name",bg="white",font=("goudy old style",18),fg="black")
name_lbl.place(x=40,y=95)

name_txt=Entry(F1,width=18,textvariable=var_name,bg="white",font=("goudy old style",18))
name_txt.place(x=180,y=95,width=250)

price_lbl=Label(F1,text="Price",bg="white",font=("goudy old style",18),fg="black")
price_lbl.place(x=40,y=160)

price_txt=Entry(F1,width=18,textvariable=var_price,bg="white",font=("goudy old style",18))
price_txt.place(x=180,y=160,width=250)

qty_lbl=Label(F1,text="Quantity",bg="white",font=("goudy old style",18),fg="black")
qty_lbl.place(x=40,y=220)

qty_txt=Entry(F1,width=18,textvariable=var_qty,bg="white",font=("goudy old style",18))
qty_txt.place(x=180,y=220,width=250)

status_lbl=Label(F1,text="Status",bg="white",font=("goudy old style",18),fg="black")
status_lbl.place(x=40,y=280)

cmb_status=ttk.Combobox(F1,textvariable=var_status,values=("Active","Inactive"),state="readonly",justify=CENTER,font=("goudy old style",15))
cmb_status.place(x=180,y=280,width=250)
cmb_status.current(0)

save_btn=Button(F1,command=add,text="Save",width=7,font=("arial",15,"bold"),bg="grey",fg="white").place(x=40,y=370)
update_btn=Button(F1,command=update,text="Update",width=7,font=("arial",15,"bold"),bg="grey",fg="white").place(x=145,y=370)
delete_btn=Button(F1,command=delete,text="Delete",width=7,font=("arial",15,"bold"),bg="grey",fg="white").place(x=250,y=370)
clear_btn=Button(F1,command=clear,text="Clear",width=7,font=("arial",15,"bold"),bg="grey",fg="white").place(x=355,y=370)

#Search Frame
SearchFrame=LabelFrame(t,text="Search Products",font=("arial",20,"bold"),bg="white")
SearchFrame.place(x=550,y=115,width=800,height=110)

'''pcode_lbl=Label(SearchFrame,text="Product Code",bg="white",font=("goudy old style",18),fg="black",pady=5)
pcode_lbl.place(x=15,y=15)'''

cmb_search=ttk.Combobox(SearchFrame,textvariable=var_search,values=("Select","Product Name","Product Code"),state="readonly",justify=CENTER,font=("goudy old style",15))
cmb_search.place(x=15,y=15,width=250)
cmb_search.current(0)

search_txt=Entry(SearchFrame,width=18,textvariable=var_search_product,bg="white",font=("goudy old style",18))
search_txt.place(x=290,y=15,width=250)

search_btn=Button(SearchFrame,command=search,text="Search",width=7,font=("arial",13,"bold"),bg="grey",fg="white").place(x=570,y=15)
show_btn=Button(SearchFrame,command=show,text="Show all",width=7,font=("arial",13,"bold"),bg="grey",fg="white").place(x=680,y=15)

#Frame to view products
F2=Frame(t,bg="white",bd=5,relief=RIDGE)
F2.place(x=550,y=250,width=700,height=390)

scrolly=Scrollbar(F2,orient=VERTICAL)
scrollx=Scrollbar(F2,orient=HORIZONTAL)

product_table=ttk.Treeview(F2,columns=("pcode","pname","quantity","price",'status'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
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

product_table.column("pcode",width=5)
product_table.column("pname",width=130)
product_table.column("quantity",width=5)
product_table.column("price",width=5)
product_table.column("status",width=5)

product_table.pack(fill=BOTH,expand=1)

product_table.bind("<ButtonRelease-1>",get_data)

cart_img=ImageTk.PhotoImage(Image.open("cart.jpg"))
cart_lbl=Label(t,image=cart_img).place(x=1275,y=300)

quit_button=Button(t,text="Exit",command=exit,width=10,font=("arial",15,"bold"),bg="grey",fg="white").place(x=1260,y=450)

show()

t.mainloop()
