
import tkinter as tk
from tkinter import messagebox,ttk
from PIL import Image,ImageTk
from datetime import datetime
import sqlite3
conn=sqlite3.connect("inventory.db")
cur=conn.cursor()


## FRONT 
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1360x800")
font_style= ("Cambria Math",30)
root.config(bg="lightgreen")
    


## UNIT OF MEASURE
def open_unit():
    root_unit=tk.Toplevel()
    root_unit.title("Unit Measures")
    root_unit.geometry("500x300")
    font_style= ("Cooper",12)
    root_unit.config(bg="#0b9e37")

    root_unit.update_idletasks()
    width=300
    height=300
    x=(root_unit.winfo_screenwidth()//2)-(width//2)
    y=(root_unit.winfo_screenheight()//2)-(height//2)
    root_unit.geometry(f"{width}x{height}+{x}+{y}")



    

    
    def savedata():
        cur.execute("INSERT INTO unit VALUES(?,?)",(str.upper(Formal_Namevar.get()),str.upper(Full_Namevar.get())))
        conn.commit()
        messagebox.showinfo(" DATA SAVED","Your Data Saved Sucessfully")
        cleardata()

    def searchdata():
        cur.execute("SELECT * from  unit WHERE Formal_Name=?",(str.upper(Formal_Namevar.get()),))
        row=cur.fetchone()
        if row:
            Full_Namevar.set(row[1])
        else:
            messagebox.showinfo(" Search not Found"," Record not Found")
            cleardata()


    def deletedata():
        cur.execute("delete from unit  WHERE Formal_Name=?",(str.upper(Formal_Namevar.get()),))
        conn.commit()
        messagebox.showinfo("DATA DELETE", "Data has Been Deleted ")
        cleardata()

    def updatedata():
        cur.execute(" update unit set Full_Name=? where Formal_Name=?",(str.upper(Formal_Namevar.get()),str.upper(Full_Namevar.get()),))
        conn.commit()
        messagebox.showinfo("RECORD UPDATED ", "Record has been update")
        cleardata()

    def cleardata():
        
        Formal_Namevar.set("")
        Full_Namevar.set("")

    Formal_Namevar=tk.StringVar()
    Full_Namevar=tk.StringVar()
    
    tk.Label(root_unit,text="Unit Measures",font=("cooper",15),bg="#0b9e37").grid(row=0,column=0,sticky="nsew")

    tk.Label(root_unit,text="Formal Name",font=("cooper",15),bg="#0b9e37").grid(row=1,column=0)
    tk.Entry(root_unit,textvariable=Formal_Namevar).grid(row=1,column=1,padx=10,pady=5)

    tk.Label(root_unit,text="Full Name",font=("cooper",15),bg="#0b9e37").grid(row=2,column=0)
    tk.Entry(root_unit,textvariable=Full_Namevar).grid(row=2,column=1,padx=10,pady=5)

    tk.Button(root_unit,text="Save",command=savedata,bg="White",font=("Arial",12)).grid(row=6,column=0,padx=10,pady=5)
    tk.Button(root_unit,text="Search ",command=searchdata,bg="White",font=("Arial",12)).grid(row=6,column=1,padx=10,pady=5)
    tk.Button(root_unit,text="Delete",command=deletedata,bg="White",font=("Arial",12)).grid(row=7,column=0,padx=10,pady=5)
    tk.Button(root_unit,text="update",command=updatedata,bg="White",font=("Arial",12)).grid(row=7,column=1,padx=10,pady=5)



## STOCK ITEM
def open_stock():
    root_stock=tk.Toplevel()
    root_stock.title("Stock items")
    root_stock.geometry("500x500")
    font_style= ("Cooper",50)
    root_stock.config(bg="#0b9e37")

    root_stock.update_idletasks()
    width=500
    height=500
    x=(root_stock.winfo_screenwidth()//2)-(width//2)
    y=(root_stock.winfo_screenheight()//2)-(height//2)
    root_stock.geometry(f"{width}x{height}+{x}+{y}")
    

    cur.execute("SELECT category_Name FROM category")
    results = cur.fetchall()
    category_list= [row[0] for row in results]
    

    cur.execute("SELECT Unit_Name FROM stock")
    results=cur.fetchall()
    stock_list= [row[0] for row in results]
    
    def savedata():
        try:
            cur.execute("INSERT INTO stock VALUES(?,?,?,?,?,?)",(str.upper(Item_Namevar.get()),str.upper( Unit_Namevar.get()),str.upper( Categoryvar.get()),Opening_itemvar.get(),Pricevar.get(),GST_Ratevar.get()))
            conn.commit()
            messagebox.showinfo(" DATA SAVED","Your Data Saved Sucessfully")
        
        except Exception as e:
               messagebox.showerror("Error", str(e))
               cleardata()
         

    def searchdata():
        cur.execute("SELECT * from  stock WHERE Item_Name=?",(str.upper(Item_Namevar.get()),))
        row=cur.fetchone()
        if row:
             Unit_Namevar.set(row[1])
             Categoryvar.set(row[2])
             Opening_itemvar.set(row[3])
             Pricevar.set(row[4])
             GST_Ratevar.set(row[5])
        else:
            messagebox.showinfo(" Search not Found"," Record not Found")
            cleardata()


    def deletedata():
        cur.execute("delete from stock WHERE Item_Name=?",(str.upper(Item_Namevar.get()),)) 
        conn.commit()
        messagebox.showinfo("DATA DELETE", "Data has Been Deleted ")
        cleardata()

    def updatedata():
        cur.execute(" update stock set Unit_Name=?,category=?,Opening_item=?,price=?,GST_Rate=? where  Item_Name=?",(str.upper(Item_Namevar.get()),str.upper( Unit_Namevar.get()), str.upper(Categoryvar.get()), Opening_itemvar.get(),Pricevar.get(),GST_Ratevar.get(),))
        conn.commit()
        messagebox.showinfo("RECORD UPDATED ", "Record has been update")
        cleardata()

    def cleardata():
        
       Item_Namevar.set("")
       Unit_Namevar.set("")
       Categoryvar.set("")
       Opening_itemvar.set("")
       Pricevar.set("")
       GST_Ratevar.set("")
       

    Item_Namevar=tk.StringVar()
    Unit_Namevar=tk.StringVar()
    Categoryvar=tk.StringVar()
    Opening_itemvar=tk.StringVar()
    Pricevar=tk.StringVar()
    GST_Ratevar=tk.StringVar()
    
    
    tk.Label(root_stock,text="Stock Items",font=("cooper",20),pady=50,padx=50,bg="#0b9e37").grid(row=0,column=0,sticky="nsew")

    tk.Label(root_stock,text="Item Name",font=("cooper",20),bg="#0b9e37").grid(row=1,column=0)
    tk.Entry(root_stock,textvariable=Item_Namevar,width=30).grid(row=1,column=1)

    tk.Label(root_stock,text="Unit Name",font=("cooper",20),bg="#0b9e37").grid(row=2,column=0)
    ttk.Combobox(root_stock,textvariable=Unit_Namevar,width=30,values= stock_list).grid(row=2,column=1)

    tk.Label(root_stock,text="Category Name",font=("cooper",20),bg="#0b9e37").grid(row=3,column=0)
    ttk.Combobox(root_stock,textvariable= Categoryvar,width=30,values=category_list).grid(row=3,column=1)

    tk.Label(root_stock,text="Opening item ",font=("cooper",20),bg="#0b9e37").grid(row=4,column=0)
    tk.Entry(root_stock,textvariable= Opening_itemvar,width=30).grid(row=4,column=1)

    tk.Label(root_stock,text="Price ",font=("cooper",20),bg="#0b9e37").grid(row=5,column=0)
    tk.Entry(root_stock,textvariable= Pricevar,width=30).grid(row=5,column=1)

    tk.Label(root_stock,text="GST Rate ",font=("cooper",20),bg="#0b9e37").grid(row=6,column=0)
    tk.Entry(root_stock,textvariable= GST_Ratevar,width=30).grid(row=6,column=1)


    tk.Button(root_stock,text="Save",command=savedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=8,column=0)
    tk.Button(root_stock,text="Search ",command=searchdata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=8,column=1)
    tk.Button(root_stock,text="Delete",command=deletedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=9,column=0)
    tk.Button(root_stock,text="update",command=updatedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=9,column=1)



### CATEGORY

def open_category():
    root_category=tk.Toplevel()
    root_category.title("Category")
    root_category.geometry("500x300")
    font_style= ("Cooper",30)
    root_category.config(bg="#0b9e37")


    root_category.update_idletasks()
    width=400
    height=400
    x=(root_category.winfo_screenwidth()//2)-(width//2)
    y=(root_category.winfo_screenheight()//2)-(height//2)
    root_category.geometry(f"{width}x{height}+{x}+{y}")
    
    
    
    def savedata():
        try:
            cur.execute("INSERT INTO category VALUES(?,?)",(str.upper(category_Namevar.get()),str.upper(category_fullNamevar.get())))
            conn.commit()
            messagebox.showinfo(" DATA SAVED","Your Data Saved Sucessfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            cleardata()
         

    def searchdata():
        cur.execute("SELECT * from  category WHERE category_Name=?",(str.upper(category_Namevar.get()),))
        row=cur.fetchone()
        if row:
            category_fullNamevar.set(row[1])
        else:
            messagebox.showinfo(" Search not Found"," Record not Found")
            cleardata()


    def deletedata():
        cur.execute("delete from category  WHERE category_Name=?",(str.upper(category_Namevar.get()),))
        conn.commit()
        messagebox.showinfo("DATA DELETE", "Data has Been Deleted ")
        cleardata()

    def updatedata():
        cur.execute(" update category set category_fullName=? where category_Name=?",(str.upper(category_Namevar.get()),str.upper(category_fullNamevar.get()),))
        conn.commit()
        messagebox.showinfo("RECORD UPDATED ", "Record has been update")
        cleardata()

    def cleardata():
        
        category_Namevar.set("")
        category_fullNamevar.set("")

    category_Namevar=tk.StringVar()
    category_fullNamevar=tk.StringVar()
    
    tk.Label(root_category,text="CATEGORY",font=("Arial",20),pady=50,padx=50,bg="#0b9e37").grid(row=0,column=0,sticky="nsew")

    tk.Label(root_category,text="category Name",font=("cooper",20),bg="#0b9e37").grid(row=1,column=0)
    tk.Entry(root_category,textvariable=category_Namevar,width=20).grid(row=1,column=1)

    tk.Label(root_category,text="category Full Name",font=("cooper",20),bg="#0b9e37").grid(row=2,column=0)
    tk.Entry(root_category,textvariable=category_fullNamevar,width=20).grid(row=2,column=1)

    tk.Button(root_category,text="Save",command=savedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=7,column=0)
    tk.Button(root_category,text="Search ",command=searchdata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=7,column=1)
    tk.Button(root_category,text="Delete",command=deletedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=8,column=0)
    tk.Button(root_category,text="update",command=updatedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=8,column=1)



## GODOWN
    
def open_godown():
    root_godown=tk.Toplevel()
    root_godown.title("godown")
    root_godown.geometry("500x400")
    font_style= ("Cooper",50)
    root_godown.config(bg="#0b9e37")

    root_godown.update_idletasks()
    width=400
    height=400
    x=(root_godown.winfo_screenwidth()//2)-(width//2)
    y=(root_godown.winfo_screenheight()//2)-(height//2)
    root_godown.geometry(f"{width}x{height}+{x}+{y}")
    
    
    
    
    
    def savedata():
        cur.execute("INSERT INTO godown VALUES(?,?,?)",(str.upper(godown_Namevar.get()),str.upper(godown_typevar.get()),str.upper(Addressvar.get())))
        conn.commit()
        messagebox.showinfo(" DATA SAVED","Your Data Saved Sucessfully")
        cleardata()

    def searchdata():
        cur.execute("SELECT * from  godown WHERE godown_Name=?",(str.upper(godown_Namevar.get()),))
        row=cur.fetchone()
        if row:
            godown_typevar.set(row[1])
            Addressvar.set(row[2])
        else:
            messagebox.showinfo(" Search not Found"," Record not Found")
            cleardata()


    def deletedata():
        cur.execute("delete from godown WHERE godown_Name=?",(str.upper(godown_Namevar.get()),))
        conn.commit()
        messagebox.showinfo("DATA DELETE", "Data has Been Deleted ")
        cleardata()

    def updatedata():
        cur.execute(" update godown set godown_type=?,Address=? where godown_Name=?",(str.upper(godown_Namevar.get()),str.upper(godown_typevar.get()),str.upper(Addressvar.get()),))
        conn.commit()
        messagebox.showinfo("RECORD UPDATED ", "Record has been update")
        cleardata()

    def cleardata():
        
        godown_Namevar.set("")
        godown_typevar.set("")
        Addressvar.set("")

    godown_Namevar=tk.StringVar()
    godown_typevar=tk.StringVar()
    Addressvar=tk.StringVar()
    
    tk.Label(root_godown,text="GODOWN",font=("Arial",20),pady=50,padx=50,bg="#0b9e37").grid(row=0,column=0,sticky="nsew")

    tk.Label(root_godown,text="godown Name",font=("cooper",20),bg="#0b9e37").grid(row=1,column=0)
    tk.Entry(root_godown,textvariable= godown_Namevar,width=30).grid(row=1,column=1)

    tk.Label(root_godown,text="godown type",font=("cooper",20),bg="#0b9e37").grid(row=2,column=0)
    tk.Entry(root_godown,textvariable=godown_typevar,width=30).grid(row=2,column=1)

    tk.Label(root_godown,text="Address",font=("cooper",20),bg="#0b9e37").grid(row=3,column=0)
    tk.Entry(root_godown,textvariable=Addressvar,width=30).grid(row=3,column=1)

    tk.Button(root_godown,text="Save",command=savedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=6,column=0)
    tk.Button(root_godown,text="Search ",command=searchdata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=6,column=1)
    tk.Button(root_godown,text="Delete",command=deletedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=7,column=0)
    tk.Button(root_godown,text="update",command=updatedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=7,column=1)

#### PARTY DETAILES
def open_party():
    root_party= tk.Toplevel()
    root_party.title("party detailes")
    root_party.geometry("500x500")
    font_style= ("Cooper",50)
    root_party.config(bg="#0b9e37")
   
    def savedata():
        cur.execute("Insert into party  values(?,?,?,?,?,?)",(str.upper(Company_Namevar.get()),str.upper(Party_typevar.get()),str.upper(Addressvar.get()),str.upper(Statevar.get()),str.upper(Emailvar.get()),(Mobilevar.get())))
        conn.commit()
        messagebox.showinfo("Data saved","Data Hasbeen Saved")
        cleardata()

    def searchdata():
        cur.execute("SELECT * from party WHERE Company_Name=?",(str.upper(Company_Namevar.get()),))
        row=cur.fetchone()
        if row:
            Party_typevar.set(row[1])
            Addressvar.set(row[2])
            Statevar.set(row[3])
            Emailvar.set(row[4])
            Mobilevar.set(row[5])
        else:
            messagebox.showinfo("RECORD NOT FOUND","NO DATA")
            cleardata()

    def deletedata():
        cur.execute(" Delete from  party where Company_Name=?",(str.upper(Company_Namevar.get()),))
        conn.commit()
        messagebox.showinfo(" DATA DELETED","Data has been deleted")
        cleardata()

    def updatedata():
        cur.execute("Update  party set Party_type=?, Address=?, State=?, Email=?, Mobile=? where Company_Name=?",(str.upper(Company_Namevar.get()),str.upper(Party_typevar.get()),str.upper(Addressvar.get()),str.upper(Statevar.get()),str.upper(Emailvar.get()),Mobilevar.get(),))
        conn.commit()
        messagebox.showinfo(" DATA UPDATE", "Data has been update")
        cleardata()

    def cleardata():
        
       Company_Namevar.set("")
       Party_typevar.set("")
       Addressvar.set("")
       Statevar.set("")
       Emailvar.set("")
       Mobilevar.set("")
       

    Company_Namevar=tk.StringVar()
    Party_typevar=tk.StringVar()
    Addressvar=tk.StringVar()
    Statevar=tk.StringVar()
    Emailvar=tk.StringVar()
    Mobilevar=tk.StringVar()
    

    tk.Label(root_party,text="Party Detail",font=("Arial",20),pady=50,padx=50,bg="#0b9e37").grid(row=0,column=0,sticky="nsew")

    tk.Label(root_party,text="Company Name",font=("cooper",20),bg="#0b9e37").grid(row=1,column=0)
    tk.Entry(root_party,textvariable= Company_Namevar,width=30).grid(row=1,column=1)

    tk.Label(root_party,text="Party type",font=("cooper",20),bg="#0b9e37").grid(row=2,column=0,sticky="nsew")
    ttk.Combobox(root_party,textvariable=Party_typevar,width=30,values=['Sundry Creditor','Sundry Debtor']).grid(row=2,column=1)
    
    tk.Label(root_party,text="Adderss",font=("cooper",20),bg="#0b9e37").grid(row=3,column=0,sticky="nsew")
    tk.Entry(root_party,textvariable=Addressvar,width=30).grid(row=3,column=1)
    

    tk.Label(root_party,text="State",font=("cooper",20),bg="#0b9e37").grid(row=4,column=0,sticky="nsew")
    tk.Entry(root_party,textvariable=Statevar,width=30).grid(row=4,column=1)

    tk.Label(root_party,text="Email",font=("cooper",20),bg="#0b9e37").grid(row=5,column=0,sticky="nsew")
    tk.Entry(root_party,textvariable=Emailvar,width=30).grid(row=5,column=1)

    tk.Label(root_party,text="Mobile",font=("cooper",20),bg="#0b9e37").grid(row=6,column=0,sticky="nsew")
    tk.Entry(root_party,textvariable=Mobilevar,width=30).grid(row=6,column=1)


    
    tk.Button(root_party,text="Save",command=savedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=8,column=0)
    tk.Button(root_party,text="Search ",command=searchdata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=8,column=1)
    tk.Button(root_party,text="Delete",command=deletedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=9,column=0)
    tk.Button(root_party,text="update",command=updatedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=9,column=1)



## PURCHASE DETAIL
def open_Purchase():
    root_purch=tk.Toplevel()
    root_purch.title("purchase")
    root_purch.geometry("1360x800")
    font_style= ("Cooper",10)
    root_purch.config(bg="#0b9e37")
    
    cur.execute("SELECT Company_Name FROM  party where Party_type=?",("SUNDRY CREDITOR",))
    results = cur.fetchall()
    party_list=[row[0] for row in results]
    

    cur.execute("SELECT Item_Name from stock")
    results1=cur.fetchall()
    stock_list=[row[0] for row in results1]

    # for party detailes
    def get_Party_details(pname:str):
        cur.execute("SELECT Address, Email, Mobile FROM party WHERE Company_Name=?",(pname,))
        row=cur.fetchall()
        return row[0] if row else("","","")
    # for items
    def get_price(iname:str):
        cur.execute("SELECT Price FROM stock WHERE Item_Name=?",(iname,))
        row=cur.fetchone()
        return float(row[0]) if row else 0.0
       

    def update_stock(Item_Name,Quantity):
        if Item_Name:
            cur.execute("SELECT Opening_item from stock WHERE Item_Name=?",(Item_Name,))
            row=cur.fetchone()
            if row:
                current_Quantity=float(row[0])
                new_Quantity= current_Quantity+ float(Quantity)
                cur.execute("UPDATE stock  SET Opening_item=? WHERE Item_Name=?",(new_Quantity,Item_Name,))
                conn.commit()
    

    

   


    def savedata():
        update_stock(Itemnamevar1.get(),Quantityvar1.get())
        update_stock(Itemnamevar2.get(),Quantityvar2.get())
        update_stock(Itemnamevar3.get(),Quantityvar3.get())
        update_stock(Itemnamevar4.get(),Quantityvar4.get())
        update_stock(Itemnamevar5.get(),Quantityvar5.get())
        cur.execute("Insert into Purchase values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Billnovar.get(),DOBpurchasevar.get(),Company_Namevar.get(),Addressvar.get(),Emailvar.get(),Mobilevar.get(),Itemnamevar1.get(),Itemnamevar2.get(),Itemnamevar3.get(),Itemnamevar4.get(),Itemnamevar5.get(),Pricevar1.get(),Pricevar2.get(),Pricevar3.get(),Pricevar4.get(),Pricevar5.get(),Quantityvar1.get(),Quantityvar2.get(),Quantityvar3.get(),Quantityvar4.get(),Quantityvar5.get(),Amountvar1.get(), Amountvar2.get(), Amountvar3.get(), Amountvar4.get(), Amountvar5.get(),TotalAmount_var.get(),Costvar.get(),NetBill_var.get()))
        conn.commit()
        messagebox.showinfo("data saved","Data saved sucessfully")
        cleardata()
    
    def cleardata():
       Billnovar.set("")
       DOBpurchasevar.set("")
       Company_Namevar.set("")
       Addressvar.set("")
       Emailvar.set("")
       Mobilevar.set("")
       Pricevar1.set("")
       Pricevar2.set("")
       Pricevar3.set("")
       Pricevar4.set("")
       Pricevar5.set("")
       Itemnamevar1.set("")
       Itemnamevar2.set("")
       Itemnamevar3.set("")
       Itemnamevar4.set("")
       Itemnamevar5.set("")
       Quantityvar1.set("")
       Quantityvar2.set("")
       Quantityvar3.set("")
       Quantityvar4.set("")
       Quantityvar5.set("")
       Amountvar1.set("")
       Amountvar2.set("")
       Amountvar3.set("")
       Amountvar4.set("")
       Amountvar5.set("")
       TotalAmount_var.set("")
       Costvar.set(18)
       NetBill_var.set("")         
    

    Billnovar=tk.StringVar()
    DOBpurchasevar=tk.StringVar()
    Company_Namevar=tk.StringVar()
    Addressvar=tk.StringVar()
    Emailvar=tk.StringVar()
    Mobilevar=tk.StringVar()
    Itemnamevar1=tk.StringVar()
    Itemnamevar2=tk.StringVar()
    Itemnamevar3=tk.StringVar()
    Itemnamevar4=tk.StringVar()
    Itemnamevar5=tk.StringVar()
    Pricevar1=tk.StringVar()
    Pricevar2=tk.StringVar()
    Pricevar3=tk.StringVar()
    Pricevar4=tk.StringVar()
    Pricevar5=tk.StringVar()
    Quantityvar1=tk.StringVar()
    Quantityvar2=tk.StringVar()
    Quantityvar3=tk.StringVar()
    Quantityvar4=tk.StringVar()
    Quantityvar5=tk.StringVar()
    Amountvar1=tk.StringVar()
    Amountvar2=tk.StringVar()
    Amountvar3=tk.StringVar()
    Amountvar4=tk.StringVar()
    Amountvar5=tk.StringVar()
    TotalAmount_var=tk.StringVar()
    Costvar=tk.StringVar()
    Costvar.set(18)
    NetBill_var=tk.StringVar()                
    



    tk.Label(root_purch,text=" PURCHASE",font=("Arial",30),bg="#0b9e37").grid(row=0,column=0,sticky="nsew")
    
    tk.Label(root_purch,text="Bill no",font=("Arial",20),bg="#0b9e37").grid(row=1,column=0,sticky="nsew")
    tk.Entry(root_purch,textvariable=Billnovar,width=30).grid(row=1,column=1)
    
    
    tk.Label(root_purch,text="Date of purchase",font=("Arial",20),bg="#0b9e37").grid(row=1,column=2,sticky="nsew")
    tk.Entry(root_purch,textvariable=DOBpurchasevar,width=30).grid(row=1,column=3)

    tk.Label(root_purch,text="Company Name",font=("Arial",20),bg="#0b9e37").grid(row=2,column=0,sticky="nsew")
    Party_cb=ttk.Combobox(root_purch,textvariable=Company_Namevar,width=30,values= party_list)
    Party_cb.grid(row=2,column=1)
    ## this section to get party add mob email detailes from party firstly we make a function 
    def on_Party_selected(event=None):
        addr,mail,mob = get_Party_details(Company_Namevar.get())
        Addressvar.set(addr)
        Emailvar.set(mail)
        Mobilevar.set(mob)
    Party_cb.bind("<<ComboboxSelected>>",on_Party_selected)
    

    tk.Label(root_purch,text="Address",font=("Arial",20),bg="#0b9e37").grid(row=3,column=0,sticky="nsew")
    tk.Entry(root_purch,textvariable=Addressvar,width=30).grid(row=3,column=1)
    
    tk.Label(root_purch,text="Email",font=("Arial",20),bg="#0b9e37").grid(row=4,column=0,sticky="nsew")
    tk.Entry(root_purch,textvariable=Emailvar,width=30).grid(row=4,column=1)

    tk.Label(root_purch,text="Mobile No",font=("Arial",20),bg="#0b9e37").grid(row=4,column=2,sticky="nsew")
    tk.Entry(root_purch,textvariable=Mobilevar,width=30).grid(row=4,column=3)

    tk.Label(root_purch,text="Item Name",font=("Arial",30),bg="#0b9e37").grid(row=7,column=0)
#---------------------------------------------------------------------------------------------------------------------------------------------    
    Item1_cb=ttk.Combobox(root_purch,textvariable=Itemnamevar1,values=stock_list)
    Item1_cb.grid(row=8,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar1.get())
        print(Price)
        Pricevar1.set(str(Price))

    Item1_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)

#-------------------------------------------------------------------------------------------------------------------------------------------------
    Item2_cb=ttk.Combobox(root_purch,textvariable=Itemnamevar2,values=stock_list)
    Item2_cb.grid(row=9,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar2.get())
        print(Price)
        Pricevar2.set(str(Price))
    Item2_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)

#------------------------------------------------------------------------------------------------------------------------------------------------
    Item3_cb=ttk.Combobox(root_purch,textvariable=Itemnamevar3,values=stock_list)
    Item3_cb.grid(row=10,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar3.get())
        print(Price)
        Pricevar3.set(str(Price))
    Item3_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)
#--------------------------------------------------------------------------------------------------------------------------------------------------        
    Item4_cb=ttk.Combobox(root_purch,textvariable=Itemnamevar4,values=stock_list)
    Item4_cb.grid(row=11,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar4.get())
        print(Price)
        Pricevar4.set(str(Price))
    Item4_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)
#-----------------------------------------------------------------------------------------------------------------------------------------------
    Item5_cb=ttk.Combobox(root_purch,textvariable=Itemnamevar5,values=stock_list)
    Item5_cb.grid(row=12,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar5.get())
        print(Price)
        Pricevar5.set(str(Price))
    Item5_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)
#--------------------------------------------------------------------------------------------------------------------------------------------------    

    tk.Label(root_purch,text="Price",font=("Arial",30),bg="#0b9e37").grid(row=7,column=1)
    tk.Entry(root_purch,textvariable=Pricevar1).grid(row=8,column=1,pady=5)
    tk.Entry(root_purch,textvariable=Pricevar2).grid(row=9,column=1,pady=5)
    tk.Entry(root_purch,textvariable=Pricevar3).grid(row=10,column=1,pady=5)
    tk.Entry(root_purch,textvariable=Pricevar4).grid(row=11,column=1,pady=5)
    tk.Entry(root_purch,textvariable=Pricevar5).grid(row=12,column=1,pady=5)


    def calculate_amount(index):
        try:
            Pricevars=[Pricevar1,Pricevar2,Pricevar3,Pricevar4,Pricevar5]
            Quantiyvars=[Quantityvar1,Quantityvar2,Quantityvar3,Quantityvar4,Quantityvar5]
            Amountvars=[Amountvar1,Amountvar2,Amountvar3,Amountvar4,Amountvar5]

            Price= float(Pricevars[index-1].get() or 0)
            Quantity= int(Quantiyvars[index-1].get() or 0)
            Amount= Price *Quantity
            Amountvars[index-1].set(str(Amount))

            total= sum(float(a.get() or 0) for a  in Amountvars)
            TotalAmount_var.set(str(total))

            Cost= float(Costvar.get()or 0)
            NetBill = total +(total * Cost /100)

            NetBill_var.set(str(round(NetBill,2)))

        except Exception as e:
           messagebox.showinfo("Calculation error",str(e))


    tk.Label(root_purch,text="Quantity",font=("Arial",30),bg="#0b9e37").grid(row=7,column=2)
    Quantity_cb1=ttk.Combobox(root_purch,textvariable=Quantityvar1,values=[str(i) for i in range(1, 101)])
    Quantity_cb1.grid(row=8,column=2,pady=5)
    Quantity_cb1.bind("<<ComboboxSelected>>",lambda e:calculate_amount(1))
    def on_Itemname_selected_1(event=None):
        Price = get_price(Itemnamevar1.get())
        Pricevar1.set(str(Price))
        calculate_amount(1)
    Item1_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_1)

#-------------------------------------------------------------------------------------------------------------------------    
    Quantity_cb2=ttk.Combobox(root_purch,textvariable=Quantityvar2,values=[str(i) for i in range(1, 101)])
    Quantity_cb2.grid(row=9,column=2,pady=5)
    Quantity_cb2.bind("<<ComboboxSelected>>",lambda e:calculate_amount(2))
    def on_Itemname_selected_2(event=None):
        Price = get_price(Itemnamevar2.get())
        Pricevar2.set(str(Price))
        calculate_amount(2)
    Item2_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_2)
#---------------------------------------------------------------------------------------------------------------------

    Quantity_cb3=ttk.Combobox(root_purch,textvariable=Quantityvar3,values=[str(i) for i in range(1, 101)])
    Quantity_cb3.grid(row=10,column=2,pady=5)
    Quantity_cb3.bind("<<ComboboxSelected>>",lambda e:calculate_amount(3))
    def on_Itemname_selected_3(event=None):
        Price = get_price(Itemnamevar3.get())
        Pricevar3.set(str(Price))
        calculate_amount(3)
    Item3_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_3)
#-------------------------------------------------------------------------------------------------------------------    
    Quantity_cb4=ttk.Combobox(root_purch,textvariable=Quantityvar4,values=[str(i) for i in range(1, 101)])
    Quantity_cb4.grid(row=11,column=2,pady=5)
    Quantity_cb4.bind("<<ComboboxSelected>>",lambda e:calculate_amount(4))
    def on_Itemname_selected_4(event=None):
        Price = get_price(Itemnamevar4.get())
        Pricevar4.set(str(Price))
        calculate_amount(4)
    Item4_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_4)
#----------------------------------------------------------------------------------------------------------------------    
    Quantity_cb5=ttk.Combobox(root_purch,textvariable=Quantityvar5,values=[str(i) for i in range(1, 101)])
    Quantity_cb5.grid(row=12,column=2,pady=5)
    Quantity_cb5.bind("<<ComboboxSelected>>",lambda e:calculate_amount(5))
    def on_Itemname_selected_5(event=None):
        Price = get_price(Itemnamevar5.get())
        Pricevar5.set(str(Price))
        calculate_amount(5)
    Item5_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_5)


    tk.Label(root_purch,text="Amount",font=("Arial",30),bg="#0b9e37").grid(row=7,column=3)
    tk.Entry(root_purch,textvariable=Amountvar1).grid(row=8,column=3,pady=5)
    tk.Entry(root_purch,textvariable=Amountvar2).grid(row=9,column=3,pady=5)
    tk.Entry(root_purch,textvariable=Amountvar3).grid(row=10,column=3,pady=5)
    tk.Entry(root_purch,textvariable=Amountvar4).grid(row=11,column=3,pady=5)
    tk.Entry(root_purch,textvariable=Amountvar5).grid(row=12,column=3,pady=5)


    tk.Label(root_purch,text="Total Amount :-",font=("Arial",20),bg="#0b9e37").grid(row=16,column=2)
    tk.Entry(root_purch,textvariable=TotalAmount_var).grid(row=16,column=3,pady=5)


    tk.Label(root_purch,text="Cost  :-",font=("Arial",20),bg="#0b9e37").grid(row=17,column=2)
    tk.Entry(root_purch,textvariable=Costvar).grid(row=17,column=3,pady=5)

    tk.Label(root_purch,text="NetBill :-",font=("Arial",20),bg="#0b9e37").grid(row=18,column=2)
    tk.Entry(root_purch,textvariable=NetBill_var).grid(row= 18,column=3,pady=5)


    tk.Button(root_purch,text="Save",command=savedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=19,column=2)


# SALE
def open_sale():
    root_sale=tk.Toplevel()
    root_sale.title("SALE BILL")
    root_sale.geometry("1360x800")
    font_style=("Arial",20)
    root_sale.config(bg="#0b9e37")
    
    
    cur.execute("SELECT Company_Name FROM  party where Party_type=?",("SUNDRY DEBTOR",))
    results = cur.fetchall()
    party_list=[row[0] for row in results]


    cur.execute("SELECT Item_Name from stock")
    results1=cur.fetchall()
    stock_list=[row[0] for row in results1]

    
    # for party detailes
    def get_Party_details(pname:str):
        cur.execute("SELECT Address, Email, Mobile FROM party WHERE Company_Name=?",(pname,))
        row=cur.fetchall()
        return row[0] if row else("","","")
    # for items
    def get_price(iname:str):
        cur.execute("SELECT Price FROM stock WHERE Item_Name=?",(iname,))
        row=cur.fetchone()
        return int(row[0]) if row else 0.0
    
    def update_stock(Item_Name,Quantity):
        if Item_Name:
            cur.execute("SELECT Opening_item from stock WHERE Item_Name=?",(Item_Name,))
            row=cur.fetchone()
            if row:
                current_Quantity=float(row[0])
                new_Quantity= current_Quantity - float(Quantity)
                cur.execute("UPDATE stock  SET Opening_item=? WHERE Item_Name=?",(new_Quantity,Item_Name,))
                conn.commit()
        
    

  

   

   
    def savedata():
        update_stock(Itemnamevar1.get(),Quantityvar1.get())
        update_stock(Itemnamevar2.get(),Quantityvar2.get())
        update_stock(Itemnamevar3.get(),Quantityvar3.get())
        update_stock(Itemnamevar4.get(),Quantityvar4.get())
        update_stock(Itemnamevar5.get(),Quantityvar5.get())
        cur.execute("Insert into sale values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Billnovar.get(),DOBsalevar.get(),Company_Namevar.get(),Addressvar.get(),Emailvar.get(),Mobilevar.get(),Itemnamevar1.get(),Itemnamevar2.get(),Itemnamevar3.get(),Itemnamevar4.get(),Itemnamevar5.get(),Pricevar1.get(),Pricevar2.get(),Pricevar3.get(),Pricevar4.get(),Pricevar5.get(),Quantityvar1.get(),Quantityvar2.get(),Quantityvar3.get(),Quantityvar4.get(),Quantityvar5.get(),Amountvar1.get(), Amountvar2.get(), Amountvar3.get(), Amountvar4.get(), Amountvar5.get(),TotalAmount_var.get(),GSTvar.get(),NetBill_var.get()))
        conn.commit()
        messagebox.showinfo("data saved","Data saved sucessfully")
        cleardata()


   
    def cleardata():
       Billnovar.set("")
       DOBsalevar.set("")
       Company_Namevar.set("")
       Addressvar.set("")
       Emailvar.set("")
       Mobilevar.set("")
       Pricevar1.set("")
       Pricevar2.set("")
       Pricevar3.set("")
       Pricevar4.set("")
       Pricevar5.set("")
       Itemnamevar1.set("")
       Itemnamevar2.set("")
       Itemnamevar3.set("")
       Itemnamevar4.set("")
       Itemnamevar5.set("")
       Quantityvar1.set("")
       Quantityvar2.set("")
       Quantityvar3.set("")
       Quantityvar4.set("")
       Quantityvar5.set("")
       Amountvar1.set("")
       Amountvar2.set("")
       Amountvar3.set("")
       Amountvar4.set("")
       Amountvar5.set("")
       TotalAmount_var.set("")
       GSTvar.set(18)
       NetBill_var.set("")         
    

    Billnovar=tk.StringVar()
    DOBsalevar=tk.StringVar()
    Company_Namevar=tk.StringVar()
    Addressvar=tk.StringVar()
    Emailvar=tk.StringVar()
    Mobilevar=tk.StringVar()
    Itemnamevar1=tk.StringVar()
    Itemnamevar2=tk.StringVar()
    Itemnamevar3=tk.StringVar()
    Itemnamevar4=tk.StringVar()
    Itemnamevar5=tk.StringVar()
    Pricevar1=tk.StringVar()
    Pricevar2=tk.StringVar()
    Pricevar3=tk.StringVar()
    Pricevar4=tk.StringVar()
    Pricevar5=tk.StringVar()
    Quantityvar1=tk.StringVar()
    Quantityvar2=tk.StringVar()
    Quantityvar3=tk.StringVar()
    Quantityvar4=tk.StringVar()
    Quantityvar5=tk.StringVar()
    Amountvar1=tk.StringVar()
    Amountvar2=tk.StringVar()
    Amountvar3=tk.StringVar()
    Amountvar4=tk.StringVar()
    Amountvar5=tk.StringVar()
    TotalAmount_var=tk.StringVar()
    GSTvar=tk.StringVar()
    GSTvar.set(18)
    NetBill_var=tk.StringVar()
    
    
    tk.Label(root_sale,text=" SALE BILL",font=("Arial",30),bg="#0b9e37").grid(row=0,column=0,sticky="nsew")

    tk.Label(root_sale,text="Bill no",font=("Arial",20),bg="#0b9e37").grid(row=1,column=0,sticky="nsew")
    tk.Entry(root_sale,textvariable=Billnovar,width=30).grid(row=1,column=1)
    
    
    tk.Label(root_sale,text="Date of sale",font=("Arial",20),bg="#0b9e37").grid(row=1,column=2,sticky="nsew")
    tk.Entry(root_sale,textvariable=DOBsalevar,width=30).grid(row=1,column=3)

    tk.Label(root_sale,text="Company Name",font=("Arial",20),bg="#0b9e37").grid(row=2,column=0,sticky="nsew")
    Party_cb=ttk.Combobox(root_sale,textvariable=Company_Namevar,width=30,values= party_list)
    Party_cb.grid(row=2,column=1)
    ## this section to get party add mob email detailes from party firsly we make a function 

    def on_Party_selected(event=None):
        addr,mail,mob = get_Party_details(Company_Namevar.get())
        Addressvar.set(addr)
        Emailvar.set(mail)
        Mobilevar.set(mob)
    Party_cb.bind("<<ComboboxSelected>>",on_Party_selected)
    

    
    tk.Label(root_sale,text="Address",font=("Arial",20),bg="#0b9e37").grid(row=3,column=0,sticky="nsew")
    tk.Entry(root_sale,textvariable=Addressvar,width=30).grid(row=3,column=1)

    tk.Label(root_sale,text="Email",font=("Arial",20),bg="#0b9e37").grid(row=4,column=0,sticky="nsew")
    tk.Entry(root_sale,textvariable=Emailvar,width=30).grid(row=4,column=1)

    tk.Label(root_sale,text="Mobile No",font=("Arial",20),bg="#0b9e37").grid(row=4,column=2,sticky="nsew")
    tk.Entry(root_sale,textvariable=Mobilevar,width=30).grid(row=4,column=3)

    tk.Label(root_sale,text="Item Name",font=("Arial",30),bg="#0b9e37").grid(row=7,column=0)

#---------------------------------------------------------------------------------------------------------------------------------------------    
    Item1_cb=ttk.Combobox(root_sale,textvariable=Itemnamevar1,values=stock_list)
    Item1_cb.grid(row=8,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar1.get())
        print(Price)
        Pricevar1.set(str(Price))

    Item1_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)

#-------------------------------------------------------------------------------------------------------------------------------------------------
    Item2_cb=ttk.Combobox(root_sale,textvariable=Itemnamevar2,values=stock_list)
    Item2_cb.grid(row=9,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar2.get())
        print(Price)
        Pricevar2.set(str(Price))
    Item2_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)

#------------------------------------------------------------------------------------------------------------------------------------------------
    Item3_cb=ttk.Combobox(root_sale,textvariable=Itemnamevar3,values=stock_list)
    Item3_cb.grid(row=10,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar3.get())
        print(Price)
        Pricevar3.set(str(Price))
    Item3_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)
#--------------------------------------------------------------------------------------------------------------------------------------------------        
    Item4_cb=ttk.Combobox(root_sale,textvariable=Itemnamevar4,values=stock_list)
    Item4_cb.grid(row=11,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar4.get())
        print(Price)
        Pricevar4.set(str(Price))
    Item4_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)
#-----------------------------------------------------------------------------------------------------------------------------------------------
    Item5_cb=ttk.Combobox(root_sale,textvariable=Itemnamevar5,values=stock_list)
    Item5_cb.grid(row=12,column=0,pady=5)
    def on_Itemname_selected(event=None):
        Price=get_price(Itemnamevar5.get())
        print(Price)
        Pricevar5.set(str(Price))
    Item5_cb.bind("<<ComboboxSelected>>",on_Itemname_selected)
#--------------------------------------------------------------------------------------------------------------------------------------------------    

    tk.Label(root_sale,text="Price",font=("Arial",30),bg="#0b9e37").grid(row=7,column=1)
    tk.Entry(root_sale,textvariable=Pricevar1).grid(row=8,column=1,pady=5)
    tk.Entry(root_sale,textvariable=Pricevar2).grid(row=9,column=1,pady=5)
    tk.Entry(root_sale,textvariable=Pricevar3).grid(row=10,column=1,pady=5)
    tk.Entry(root_sale,textvariable=Pricevar4).grid(row=11,column=1,pady=5)
    tk.Entry(root_sale,textvariable=Pricevar5).grid(row=12,column=1,pady=5)



    def calculate_amount(index):
        try:
            Pricevars=[Pricevar1,Pricevar2,Pricevar3,Pricevar4,Pricevar5]
            Quantiyvars=[Quantityvar1,Quantityvar2,Quantityvar3,Quantityvar4,Quantityvar5]
            Amountvars=[Amountvar1,Amountvar2,Amountvar3,Amountvar4,Amountvar5]

            Price= float(Pricevars[index-1].get() or 0)
            Quantity= int(Quantiyvars[index-1].get() or 0)
            Amount= Price *Quantity
            Amountvars[index-1].set(str(Amount))

            total= sum(float(a.get() or 0) for a  in Amountvars)
            TotalAmount_var.set(str(total))

            GST= float(GSTvar.get()or 0)
            NetBill = total +(total * GST /100)

            NetBill_var.set(str(round(NetBill,2)))

        except Exception as e:
           messagebox.showinfo("Calculation error",str(e))


    
    tk.Label(root_sale,text="Quantity",font=("Arial",30),bg="#0b9e37").grid(row=7,column=2)
    Quantity_cb1=ttk.Combobox(root_sale,textvariable=Quantityvar1,values=[str(i) for i in range(1, 101)])
    Quantity_cb1.grid(row=8,column=2,pady=5)
    Quantity_cb1.bind("<<ComboboxSelected>>",lambda e:calculate_amount(1))
    def on_Itemname_selected_1(event=None):
        Price = get_price(Itemnamevar1.get())
        Pricevar1.set(str(Price))
        calculate_amount(1)
    Item1_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_1)

#-------------------------------------------------------------------------------------------------------------------------    
    Quantity_cb2=ttk.Combobox(root_sale,textvariable=Quantityvar2,values=[str(i) for i in range(1, 101)])
    Quantity_cb2.grid(row=9,column=2,pady=5)
    Quantity_cb2.bind("<<ComboboxSelected>>",lambda e:calculate_amount(2))
    def on_Itemname_selected_2(event=None):
        Price = get_price(Itemnamevar2.get())
        Pricevar2.set(str(Price))
        calculate_amount(2)
    Item2_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_2)
#---------------------------------------------------------------------------------------------------------------------

    Quantity_cb3=ttk.Combobox(root_sale,textvariable=Quantityvar3,values=[str(i) for i in range(1, 101)])
    Quantity_cb3.grid(row=10,column=2,pady=5)
    Quantity_cb3.bind("<<ComboboxSelected>>",lambda e:calculate_amount(3))
    def on_Itemname_selected_3(event=None):
        Price = get_price(Itemnamevar3.get())
        Pricevar3.set(str(Price))
        calculate_amount(3)
    Item3_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_3)
#-------------------------------------------------------------------------------------------------------------------    
    Quantity_cb4=ttk.Combobox(root_sale,textvariable=Quantityvar4,values=[str(i) for i in range(1, 101)])
    Quantity_cb4.grid(row=11,column=2,pady=5)
    Quantity_cb4.bind("<<ComboboxSelected>>",lambda e:calculate_amount(4))
    def on_Itemname_selected_4(event=None):
        Price = get_price(Itemnamevar4.get())
        Pricevar4.set(str(Price))
        calculate_amount(4)
    Item4_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_4)
#----------------------------------------------------------------------------------------------------------------------   
    Quantity_cb5=ttk.Combobox(root_sale,textvariable=Quantityvar5,values=[str(i) for i in range(1, 101)])           
    Quantity_cb5.grid(row=12,column=2,pady=5)
    Quantity_cb5.bind("<<ComboboxSelected>>",lambda e:calculate_amount(5))
    def on_Itemname_selected_5(event=None):
        Price = get_price(Itemnamevar5.get())
        Pricevar5.set(str(Price))
        calculate_amount(5)
    Item5_cb.bind("<<ComboboxSelected>>", on_Itemname_selected_5)

#----------------------------------------------------------------------------------------------------------------------

    tk.Label(root_sale,text="Amount",font=("Arial",30),bg="#0b9e37").grid(row=7,column=3)
    tk.Entry(root_sale,textvariable=Amountvar1).grid(row=8,column=3,pady=5)
    tk.Entry(root_sale,textvariable=Amountvar2).grid(row=9,column=3,pady=5)
    tk.Entry(root_sale,textvariable=Amountvar3).grid(row=10,column=3,pady=5)
    tk.Entry(root_sale,textvariable=Amountvar4).grid(row=11,column=3,pady=5)
    tk.Entry(root_sale,textvariable=Amountvar5).grid(row=12,column=3,pady=5)


    tk.Label(root_sale,text="Total Amount :-",font=("Arial",20),bg="#0b9e37").grid(row=16,column=2)
    tk.Entry(root_sale,textvariable=TotalAmount_var).grid(row=16,column=3,pady=5)


    tk.Label(root_sale,text="GST  :-",font=("Arial",20),bg="#0b9e37").grid(row=17,column=2)
    tk.Entry(root_sale,textvariable=GSTvar).grid(row=17,column=3,pady=5)

    tk.Label(root_sale,text="NetBill :-",font=("Arial",20),bg="#0b9e37").grid(row=18,column=2)
    tk.Entry(root_sale,textvariable=NetBill_var).grid(row= 18,column=3,pady=5)


    tk.Button(root_sale,text="Save",command=savedata,width=10,height=2,bg="White",font=("Arial",12)).grid(row=19,column=2)

# GST

def open_GST():
    root_GST=tk.Toplevel()
    root_GST.title("GOOD SERVICES TAX")
    root_GST.geometry("500x300")
    root_GST.config(bg="#0b9e37")


    def savedata():
        try:
            cur.execute("Insert into GST values(?,?)",(str.upper(gstvar.get()),str.upper(statevar.get())))
            conn.commit()
            messagebox.showinfo("Saved","data has been saved")
            cleardata()

        except Exception as e:
            messagebox.showinfo("ERROR",str(e))
            cleardata()
    def searchdata():
        cur.execute("select * from GST where GSTNO=?",(str.upper(gstvar.get()),))
        row=cur.fetchone()
        if row:
            statevar.set(row[1])  
        else:
            messagebox.showinfo("found","no data found with this GSTNO")
            cleardata()

    def deletedata():
        cur.execute("delete from GST where gst=?",(str.upper(gstvar.get()),))
        conn.commit()
        messagebox.showinfo("deleted","record has been deleted")
        cleardata()
    

    def updatedata():
        cur.execute("Update GST set State=? where gst =?",(str.upper(gstvar.get()),str.upper(statevar.get())))
        conn.commit()
        messagebox.showinfo("update","record has been update")
        cleardata()

        
    def cleardata():
         gstvar.set("")
         statevar.set("")
        

    gstvar=tk.StringVar()
    statevar=tk.StringVar()

    tk.Label(root_GST,text="GST NO",font=("Arial",20),bg="#0b9e37").grid(row=0,column=1)

    tk.Label(root_GST,text="GST NO",font=("Arial",20),bg="#0b9e37").grid(row=2,column=0)
    tk.Entry(root_GST,textvariable=gstvar).grid(row=2,column=1)


    tk.Label(root_GST,text="State",font=("Arial",20),bg="#0b9e37").grid(row=4,column=0)
    tk.Entry(root_GST,textvariable=statevar).grid(row=4,column=1)

    tk.Button(root_GST,text="Save",command="savedata",font=("Arial",20)).grid(row=7,column=0)
    tk.Button(root_GST,text="Delete",command="deletedata",font=("Arial",20)).grid(row=7,column=1)
    tk.Button(root_GST,text="Search",command="searchdata",font=("Arial",20)).grid(row=8,column=0)
    tk.Button(root_GST,text="Update",command="updatedata",font=("Arial",20)).grid(row=8,column=1)
    root_GST.mainloop()
    
# display
def open_display():
    root_display= tk.Toplevel()
    root_display.title("DISPLAY")
    root_display.geometry("800x600")
    font_style=("Arial",20)
    root_display.config(bg="#0b9e37")

    #fetch categories
    cur.execute("SELECT category_Name FROM category")
    results = cur.fetchall()
    stock_list=[row[0] for row in results]

    categoryNamevar = tk.StringVar()
    tk.Label(root_display, text="DISPLAY", font= ("Arial",20), bg="#0b9e37", fg="white").grid(row=0, column=1, pady=10)
    tk.Label(root_display, text="Categories", font=font_style, bg="#0b9e37", fg="white").grid(row=1, column=0)

    stock_cb = ttk.Combobox(root_display, textvariable=categoryNamevar, values= stock_list, state="readonly")
    stock_cb.grid(row=1, column=1, padx=10, pady=5)

    # Configure treeview style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#ffffff", foreground="black", rowheight=25, fieldbackground="#e6ffe6")
    style.map("Treeview", background=[("selected", "#0b9e37")])

    
    # Make columns expand
    root_display.columnconfigure(0, weight=1)
    root_display.columnconfigure(1, weight=1)
    root_display.columnconfigure(2, weight=1)
    root_display.rowconfigure(3, weight=1)

    tree = ttk.Treeview(root_display, columns=("Itemname", "Price", "Quantity"), show="headings", height=15)
    tree.heading("Itemname", text="Item Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")
    #scroll bar
    
    vsb = ttk.Scrollbar(root_display, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(root_display, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=vsb.set, xscroll=hsb.set)

    tree.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
    vsb.grid(row=3, column=3, sticky='ns')
    hsb.grid(row=4, column=0, columnspan=3, sticky='ew')

    def dispaly_selected_category(event):
        selected_category = categoryNamevar.get()
        for row in tree.get_children():
            tree.delete(row)
        cur.execute("SELECT Item_Name,Opening_item,Price FROM stock WHERE Category=?",(selected_category,))
        for row in cur.fetchall():
            tree.insert("",tk.END,values=row)
    stock_cb.bind("<<ComboboxSelected>>", dispaly_selected_category)
    root_display.mainloop()

# pb
def open_purchase_bill():
    root_display= tk.Toplevel()
    root_display.title("purchase Bill")
    root_display.geometry("800x600")
    font_style=("Arial",20)
    root_display.config(bg="#0b9e37")

    cur.execute("SELECT Billno FROM Purchase")
    results = cur.fetchall()
    Party_list=[row[0] for row in results]

    Billvar = tk.StringVar()
    tk.Label(root_display, text="Puchase Bill", font= ("Arial",20), bg="#0b9e37", fg="white").grid(row=0, column=1, pady=10)
    tk.Label(root_display, text="Bill No", font=font_style, bg="#0b9e37", fg="white").grid(row=1, column=0)


    Party_cb = ttk.Combobox(root_display, textvariable= Billvar, values= Party_list, state="readonly")
    Party_cb.grid(row=1, column=1, padx=10, pady=5)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#ffffff", foreground="black", rowheight=25, fieldbackground="#e6ffe6")
    style.map("Treeview", background=[("selected", "#0b9e37")])

    # Make columns expand
    root_display.columnconfigure(0, weight=1)
    root_display.columnconfigure(1, weight=1)
    root_display.columnconfigure(2, weight=1)
    root_display.rowconfigure(3, weight=1)
    tree =ttk.Treeview(root_display,columns=("DOBpurchase","Company_Name","Address","Email","Mobile","TotalAmount","NetBill"),show="headings",height=15)
    tree.heading("DOBpurchase",text=" Date of purchase")
    tree.heading("Company_Name",text="company Name")
    tree.heading("Address",text="Address")
    tree.heading("Email",text="Email")
    tree.heading("Mobile",text="Mobile")
    tree.heading("TotalAmount",text="Total Amaount")
    tree.heading("NetBill",text="Net Bill")

    vsb = ttk.Scrollbar(root_display, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(root_display, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=vsb.set, xscroll=hsb.set)

    tree.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
    vsb.grid(row=3, column=3, sticky='ns')
    hsb.grid(row=4, column=0, columnspan=3, sticky='ew')

    def display_selected_Purchase_bill(event):
        selected_Purchase_bill= Billvar.get()
        
    
        for row in tree.get_children():
            tree.delete(row)
        cur.execute("select DOBpurchase,Company_Name,Address,Email,Mobile,TotalAmount,NetBill FROM Purchase WHERE Billno=?",(selected_Purchase_bill,))
        
            
        for row in cur.fetchall():
            tree.insert("",tk.END,values=row)
            
    Party_cb.bind("<<ComboboxSelected>>",display_selected_Purchase_bill)
    
    root_display.mainloop()






image_frame = tk.Frame(root, bg="#e0ac1b")
image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

title_label = tk.Label(image_frame, text="Inventory Management System", font=("Helvetica", 30, "bold"), bg="white", fg="#2E86C1")
title_label.pack(pady=20)

now = datetime.now().strftime("%d %B %Y, %I:%M %p")
tk.Label(image_frame, text=now, font=("Arial", 10), bg="white", fg="gray").pack()


try:
    img = Image.open("inventory.png")  
    resized_img = img.resize((1000,600), Image.Resampling.NEAREST)
    bg_img = ImageTk.PhotoImage(resized_img)
    label = tk.Label(image_frame, image=bg_img)
    label.image = bg_img  
    label.pack(pady=20)
except Exception as e:
    print("Image loading failed:", e)
    tk.Label(image_frame, text= "Image not found", font=("Arial", 16), bg="white").pack(pady=20)




# MENU BAR

menu_bar= tk.Menu(root, bg="#3498db", fg="lightgreen", activebackground="white", activeforeground="black")
menu_bar.config(bg="lightgreen")


User_menu=tk.Menu(menu_bar,tearoff=0, bg="#3498db", fg="white", activebackground="white", activeforeground="black")
User_menu.add_command(label="New")
User_menu.add_command(label="Exits")
menu_bar.add_cascade(label="User",menu=User_menu)

management_menu=tk.Menu(menu_bar,tearoff=0)
management_menu.add_command(label="Units",command=open_unit)
management_menu.add_command(label="Stock",command=open_stock)
management_menu.add_command(label="Category",command=open_category)
management_menu.add_command(label="Godown",command=open_godown)
management_menu.add_separator()
management_menu.add_command(label="GST",command=open_GST)

menu_bar.add_cascade(label="Management",menu=management_menu)


party_menu=tk.Menu(menu_bar,tearoff=0)
party_menu.add_command(label="party",command=open_party)
menu_bar.add_cascade(label="Party",menu=party_menu)


display_menu=tk.Menu(menu_bar,tearoff=0)
display_menu.add_command(label="Display",command=open_display)
display_menu.add_command(label="Purchase Bill",command=open_purchase_bill)
menu_bar.add_cascade(label="Display",menu=display_menu)


record_menu=tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="Record",menu=record_menu)

Purchase_menu=tk.Menu(menu_bar,tearoff=0)
Purchase_menu.add_command(label="bill",command=open_Purchase)
menu_bar.add_cascade(label="Purchase",menu=Purchase_menu)


sale_menu=tk.Menu(menu_bar,tearoff=0)
sale_menu.add_command(label="Sale",command=open_sale)
menu_bar.add_cascade(label="Sale",menu=sale_menu)
root.config(menu=menu_bar)

#tk.Label(root,text="Inventory Management System",font=font_style,pady=50,padx=400,bg="lightgreen",fg="blue").grid(row=1,column=1)
root.mainloop()
