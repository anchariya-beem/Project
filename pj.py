from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkinter import filedialog
from datetime import datetime
import time 
from tkinter import messagebox, Listbox ,StringVar,font
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import Toplevel, Label, Entry, Button, filedialog
import tkinter.font as tkFont
from tkinter import filedialog
import io
from io import BytesIO
from tkinter import font as tkFont
import requests
import numpy as np
import cv2
from tkinter import Canvas, Scrollbar
import re
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

db_file = r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db"

cart_items = []
total_price = 0
total = 0                               
image_tk = None  # เริ่มต้นอ็อบเจ็กต์ ImageTk ในสภาวะว่าง
receipt_window = None  # เรียกใช้ตัวแปร global receipt_window
order_items = []


def exit_officer(myofficer):
    myofficer.withdraw()
    root.deiconify()

#menushow
def open_menushow(): 
    def order_show_product():
            conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM store ")
            pictures = cursor.fetchall()
            cart = {}
            def addtocart(item):
                def add():
                    c = conn.cursor()
                    c.execute("INSERT INTO myorder (name, price, picture) VALUES (?, ?, ?)", (item[1], item[2], item[3]))
                    conn.commit()
                    add_to_cart()
                return add

            for i, x in enumerate(pictures):    #แปลงภาพ
                image = Image.open(BytesIO(x[3]))
                target_width, target_height = 120, 120  #กำหนดขนาดเป้าหมายของรูปภาพที่ต้องการ (ในที่นี้คือ 128x128 พิกเซล)
                image = image.resize((target_width, target_height))   #ปรับขนาดรูปภาพให้ตรงกับขนาดเป้าหมาย
                image = ImageTk.PhotoImage(image)    #แปลงรูปภาพ Pillow เป็น ImageTk.PhotoImage


                label = Button(product, image=image, text=" {}  ฿ {} ".format(x[1], x[2]), compound="top", command=addtocart(x), bg= "#76B666", fg="white",font=14)
                label.image = image
                label.grid(row=i // 3, column=i % 3, padx=10, pady=10)
    
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    root.withdraw()
    menu = tk.Toplevel()
    menu.title('เมนูmilk corner')
    menu.geometry('1000x650+100+100')
    menu.resizable(False, False)
    menu.configure(bg=('#F6C8B6'))
    background1_image = Image.open(r'c:\Users\Thirawat\Downloads\CUSTOMER (5).png')
    background1_image = background1_image.resize((1012, 665))
    background1_photo = ImageTk.PhotoImage(background1_image)
    background1_label = Label(menu, image=background1_photo)
    background1_label.image = background1_photo
    background1_label.pack()
    
    canvas = Canvas(menu, bg="#F7FFE3")  # สร้าง Canvas
    canvas.place(x=50, y=100, width=560, height=450)

    # เพิ่ม scrollbar ในแนวแกน Y (ตั้ง)
    scrollbar = Scrollbar(menu, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)  # เชื่อม scrollbar กับ Canvas

    product = Frame(canvas, bg="#F7FFE3")
    canvas.create_window((0, 0), window=product, anchor='nw')

    menu.bind("<MouseWheel>", on_mousewheel)
    order_show_product()
      

    #แสดงสินค้าที่เพิ่ม
    for item in order_items:
        item_label = Label(menu, text=f"{item['name']} - {item['price']} บาท", font=('arial', 12), bg='#E6E6E6')
        item_label.pack()
    
        #เพิ่มเข้าตะกร้า 
    def add_to_cart():    #เพิ่มสินค้าและราคาลงในตะกร้าสินค้า 
        global total_price
        global cart_items
        total_price =0
        cart_items =[]
        conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
        cursor = conn.cursor() 
        cursor.execute("SELECT name ,price FROM myorder")
        order = cursor.fetchall()

        for item_name,item_price in order:

            cart_items.append((item_name,item_price))
                
            total_price += item_price
            
            
            cart_listbox.delete(0,END) 
            for (name, price) in (cart_items):
                item_text = f"        {name}             {price:.2f} บาท" #สร้างข้อความรายการสินค้าที่แสดงใน cart_listbox
                cart_listbox.insert(tk.END, item_text)
        # update_cart_listbox()   #อัปเดตแสดงรายการสินค้าในตะกร้า
        update_total_label()    #อัปเดตแสดงราคารวม
        
        
    #ลบของออกจากตะกร้าลดยอดรวมและอัปเดตการแสดงผลของรายการในตะกร้าและยอดรวมทั้งหมด
    def remove_from_cart():
        global total_price
        conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
        cursor = conn.cursor() 
        cursor.execute('''DELETE FROM myorder''')
        conn.commit()
        cart_items.clear()
        total_price = 0
        cart_listbox.delete(0, tk.END)

        # update_cart_listbox()
        update_total_label()


    def remove_selected_item():
        remove_from_cart()  # เรียกใช้ฟังก์ชัน remove_from_cart โดยส่ง index ของรายการที่ถูกเลือกไปเพื่อลบรายการนั้นออกจากตะกร้าสินค้า (cart).
        total = sum(sinka[1] for sinka in cart_items)
        
        if total >= 0:
            discount =0  
            total -= discount
        else:
            discount = 0
            pass

    remove_button = tk.Button(menu, text="ลบรายการ", command=remove_selected_item,font=("Tahoma", 13),bg="#F7FFE3")
    remove_button.pack()
    remove_button.place(x=710, y=493)
    
    def generate_receipt(items, total, discount):
        global receipt_window 

        named_tuple = time.localtime()  # get struct_time
        time_string = time.strftime("%d/%m/%Y", named_tuple)

        named_tuple1 = time.localtime()  # get struct_time
        time_string1 = time.strftime("%m/%Y", named_tuple1)

        receipt_window = Toplevel(root)
        receipt_window.title("ใบเสร็จ")
        receipt_window.geometry("400x650+450+150")
        receipt_window.resizable(False, False)
        
        # สร้าง Label และเก็บ bill_now ในตัวแปร label
        label = Label(receipt_window)
        label.place(x=0, y=0)  # ระบุตำแหน่ง x และ y ที่ต้องการแสดง Label

        receipt = f"รายการทั้งหมด\n\n"
        for item, price in items:
            receipt += f"{item}           {price:.2f} บาท\n"
        receipt += f"\n\n\nยอดรวม         {total_price:.2f} บาท\n"
        priceprice=total_price 
        receipt += f"ยอดสุทธิ               {priceprice:.2f} บาท\n\n"
        receipt += f"{time_string}"

        # แสดงใบเสร็จใน Label
        receipt_label = Label(receipt_window, text=receipt, font=("Tahoma", 13),bg="#F7FFE3")
        receipt_label.configure(height=350, width=450)
        # receipt_label.place(x=90, y=127)
        receipt_label.pack()


        # URL ของรูปภาพรหัส QR# URL of the QR code image
        text = "https://promptpay.io/0889681233/" + str(priceprice) + ".png"
        image_url = text

        # ส่งคำขอดาวน์โหลดภาพ
        response = requests.get(image_url)

        # ตรวจสอบว่าคำขอสำเร็จหรือไม่ (รหัสสถานะ HTTP 200)
        if response.status_code == 200:
            # Open the image using PIL
            image = Image.open(BytesIO(response.content))
            
            # แปลงรูปภาพเป็นโทนสีเทาหากยังไม่ได้ทำ
            if image.mode != 'L':
                image = image.convert('L')
            
            # แปลงอิมเมจ PIL เป็นอาร์เรย์ NumPy
            img_np = np.array(image)

            # เริ่มต้นเครื่องตรวจจับ QRCode
            qr_decoder = cv2.QRCodeDetector()

            # ตรวจจับและถอดรหัสรหัส QR
            val = qr_decoder.detectAndDecode(img_np)

            # พิมพ์ค่าที่ถอดรหัสจากรหัส QR
            print("Decoded value from the QR code:", val)

            # แสดงภาพในหน้าต่าง Tkinter
            img_tk = ImageTk.PhotoImage(image)
            label = Label(receipt_window, image=img_tk)
            label.image = img_tk
            new_width = 150  # Adjust the desired width
            new_height = 150  # Adjust the desired height
            qr_image_resized = image.resize((new_width, new_height))
            img_tk_resized = ImageTk.PhotoImage(qr_image_resized)
            label_resized = Label(receipt_window, image=img_tk_resized)
            label_resized.image = img_tk_resized  # Keep a reference to avoid garbage collection
            label_resized.place(x=125, y=25)
        else:
            print("Failed to download the image. HTTP status code:", response.status_code)
        
 
        

        def backto_menu_from_receipt():
            timenow = datetime.now().strftime("%H:%M:%S")
            conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
            cursor = conn.cursor() 
            cursor.execute("INSERT INTO bill (order_total,date,price,month) VALUES (?, ?, ?,?)", (receipt, time_string,priceprice,time_string1))
            conn.commit()
            
            receipt_window.destroy()  # ทำลายหน้าใบเสร็จ
            menu.deiconify()  # แสดงหน้าเมนูอีกครั้ง
            
            cursor.execute("SELECT COUNT(id) FROM bill;")
            count_all = cursor.fetchone()[0]
            
            pdfmetrics.registerFont(TTFont('THSarabun', r"C:\Users\Thirawat\Downloads\th-sarabun-psk\THSarabun.ttf"))

            doc = SimpleDocTemplate("invoiceID%s.pdf"%f"{count_all}", pagesize=letter)

            elements = []

            
            styles = getSampleStyleSheet()
            normal_style_head = styles['Normal']
            normal_style_head.fontName = 'THSarabun'  
            normal_style_head.fontSize = 20


            styles = getSampleStyleSheet()
            normal_style1 = styles['Normal']
            normal_style1.fontName = 'THSarabun'  
            normal_style1.fontSize = 30

            styles = getSampleStyleSheet()
            normal_style2 = styles['Normal']
            normal_style2.fontName = 'THSarabun'  
            normal_style2.fontSize = 25
            
            styles = getSampleStyleSheet()
            normal_style3 = styles['Normal']
            normal_style3.fontName = 'THSarabun'  
            normal_style3.fontSize = 13


            #สร้างคำในใบเสร็จ
            head = Paragraph("ใบเสร็จรับเงิน", normal_style1)
            head1 = Paragraph("Milk corner", normal_style1)
            datepdf = Paragraph("วันที่ : %s"%time_string, normal_style_head)
            time = Paragraph("เวลาที่ : %s"%timenow, normal_style_head)
            line = Paragraph("________________________________________________________________", normal_style_head)
            pos = Paragraph("รายการ ", normal_style2)
            menus = Paragraph("%s" %cart_items,normal_style3)
            postid = Paragraph("ยอดรวม : %s"%priceprice, normal_style2)
          


            spacer = Spacer(1, 10)  
            spacer1 = Spacer(1, 50)
            spacer2 = Spacer(1, 20)


            elements.append(head)
            elements.append(spacer1)
            elements.append(head1)
            elements.append(spacer)
            elements.append(spacer1)
            elements.append(datepdf)
            elements.append(spacer)
            elements.append(time)
            elements.append(line)
            elements.append(spacer2)
            elements.append(pos)
            elements.append(spacer2)
            elements.append(menus)
            elements.append(spacer2)
            elements.append(postid)
            elements.append(spacer2)
            elements.append(line)
            doc.build(elements)

            #เปิดสลิปpdf
            subprocess.Popen(["start", "invoiceID%s.pdf"%f"{count_all}"], shell=True)
            
            
            

        back_from_receipt_button = tk.Button(receipt_window, text="จ่ายเงินเรียบร้อย", command=backto_menu_from_receipt, font=("Tahoma", 10), bg="#FF99CC", highlightthickness=0, bd=0)
        back_from_receipt_button.place(x=145, y=550)
        receipt_window.protocol("WM_DELETE_WINDOW", clearlist)
        
    def checkout():
        total = sum(sinka[1] for sinka in cart_items)   
        discount = 0
    
        if total >= 0:
            discount = 0    
            total -= discount

        global receipt_window #นี้คือการแน่ใจว่า receipt_window ถูกกำหนดค่าในฟังก์ชัน generate_receipt และเมื่อถูกเรียกใช้ในฟังก์ชัน clearlist มันจะถูกทำลาย (destroy) อย่างถูกต้องเมื่อมีค่าเป็นหน้าต่าง Toplevel ที่ถูกสร้างขึ้นแล้ว และไม่มีข้อผิดพลาดในการเรียกใช้ generate_receipt และ checkout
        generate_receipt(cart_items, total, discount)    #เรียกใช้ฟังก์ชัน generate_receipt เพื่อสร้างใบเสร็จโดยส่ง cart_items, total, และ discount เป็นพารามิเตอร์.
        
        
    checkout_button = tk.Button(menu, text="ชำระเงิน", command=checkout,font=("Tahoma", 12),bg="#F7FFE3")
    checkout_button.pack()
    checkout_button.place(x=720, y=545)

    def backto_menu():  # สร้างฟังก์ชันเพื่อกลับไปที่หน้าหลัก
        menu.destroy()  # ทำลายหน้าเมนูปัจจุบัน
        root.deiconify()
        
    back = tk.Button(menu, text="BACK HOME", command=backto_menu,font=("Tahoma", 13),relief="sunken", bg="#F7FFE3", highlightthickness=2, bd=2)
    back.place(x=9, y=8)
    



    def clearlist(): #เคลียร์ของในlistbox
        global total_price
        global receipt_window  # เรียกใช้ตัวแปร global receipt_window
        while len(cart_items) > 0:   
            item_name, item_price = cart_items.pop()  #เอาข้อมูลรายการสินค้าออกมาเก็บในitem_name, item_price แล้วทำให้เป็น0
            item_name = 0
            item_price = 0
            total_price = 0
            update_total_label()
            conn = sqlite3.connect('newprojectgood.db')
            cursor = conn.cursor() 
            cursor.execute('''DELETE FROM myorder ''')
            conn.commit()
            cart_listbox.delete(0,END)  #ล้างข้อมูลใน GUI
            receipt_window.destroy()
        

    def update_total_label():
        total_ver.set(f"รวมทั้งหมด{total_price:.2f} บาท")
        total_label.config(font=("Tahoma", 12),bg="#F7FFE3")
        total_label.place(x=640,y=440)

    #แสดงรายการในรถเข็น
    cart_listbox = Listbox(menu, width=25, height=15,font=16,bg="#F7FFE3")
    cart_listbox.place(x=630, y=100)
    

    total_ver = StringVar()
    total_label = tk.Label(menu, textvariable=total_ver, font=("Arial", 12))
    total_label.pack()
    total_label.place(x=600, y=450)
    
    menu.mainloop()
    
# หน้าต่างผู้พัฒนา
def show_developer_info():
        developer_info_window = Toplevel(root)
        developer_info_window.title("ข้อมูลผู้พัฒนา")
        developer_info_window.geometry('800x600+350+100')
        developer_info_window.resizable(FALSE,FALSE)
        developer_info_window.configure(background='light sky blue')
        # โหลดรูปภาพและแปลงเป็น ImageTk.PhotoImage
        img_path = r'c:\Users\Thirawat\Downloads\อัญฉริญา ทองดี.png'
        img = Image.open(img_path)
        img = ImageTk.PhotoImage(img)
        # แสดงรูปภาพใน Label
        img_label = Label(developer_info_window, image=img, bg='white')
        img_label.pack()
        developer_info_window.image = img  # เก็บอ้างอิงไว้เพื่อไม่ให้รูปถูกทำลายเมื่อฟังก์ชันจบ
        
        def home():
            developer_info_window.withdraw()
            root.deiconify()
        ok_button = tk.Button(developer_info_window, text="BACK",relief="sunken", font=("Tahoma", 10),command=home, width=5,height=2, bg='white',)
        ok_button.place(x=370,y=550)
        
    
def checkint(P):  #ตรวจสอบ
    if P.isdigit() or P == "":
        return True
    else:
        return False 
z=[]

def add():
    name = editnamemanu_entry.get()
    price = pricemenu_entry.get()
    

    file_ = filedialog.askopenfilename()
    if file_:
        with open(file_, 'rb')as file:
            picture = file.read()
    if name and price  and picture:
        conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO store (name, price,picture) VALUES (?, ?, ?)", (name, price, picture))        
        conn.commit()
        
        editnamemanu_entry.delete(0, tk.END) 
        pricemenu_entry.delete(0, tk.END)
        show()



def delete():
    selected_product = products_listbox.curselection()
    if selected_product:
        a = selected_product[0]
        product_id = z[a]
        conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM store WHERE id=?", (product_id,))
        conn.commit()
        show() 
        

def show():
    products_listbox.delete(0,tk.END)
    conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM store''')
    result = c.fetchall()
    i =1 
    z.clear()
    for x in result:
        products_listbox.delete(0, tk.END)
        c=conn.cursor()   
        c.execute('''SELECT * FROM store''')
        result=c.fetchall()
        i=1
        z.clear()
        for x in result:
            products_listbox.insert(x[0]," Product No:  {}    {}    price:  {}  ".format(i,x[1],x[2]))
            z.append(x[0])
            i+=1



def edit():
    selected_product = products_listbox.curselection()
    if selected_product:
        a = selected_product[0]
        idedit = z[a]
        name = editnamemanu_entry.get()
        price = pricemenu_entry.get()
        file_pic = filedialog.askopenfilename()
        if file_pic:
            with open(file_pic, 'rb') as file:
                picture = file.read()
        conn = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
        cursor = conn.cursor()      
        cursor.execute('''UPDATE store SET name =?,price =?,picture=? WHERE id =? ''',(name, price, picture, idedit))
        editnamemanu_entry.delete(0, tk.END)
        pricemenu_entry.delete(0, tk.END)
        conn.commit()
        show()
        
def show_edit():
    def edit_manu():
        global products_listbox, editnamemanu_entry, pricemenu_entry, z, edit_manu
        edit_manu = tk.Toplevel(root)
        edit_manu.title("แก้ไขข้อมูลสินค้า")
        edit_manu.geometry('1000x650+100+100')
        edit_manu.resizable(False, False)
        img = Image.open(r'c:\Users\Thirawat\Downloads\CUSTOMER (5).png')
        img = img.resize((1000, 650))
        photo = ImageTk.PhotoImage(img)
        img_label1 = Label(edit_manu, image=photo)
        img_label1.photo = photo 
        img_label1.place(x=0,y=0)

        editnamemanu_entry = tk.Entry(edit_manu)
        editnamemanu_entry.place(x=240,y=175, width=250, height=50)
        
        # editnamemanu_entry.config(background='#E09B80')
        validate_func = edit_manu.register(checkint)
        pricemenu_entry = tk.Entry(edit_manu,validate='key',validatecommand=(validate_func,'%P'))  # ใส่ show="*" เพื่อซ่อนรหัสผ่าน
        pricemenu_entry.place(x=240,y=285,width=250, height=50)
        
        re_button =tk.Button(edit_manu,text='Refresh',command=show)
        re_button.place(x=100, y=0, width=50, height=50)
        
        add_button =tk.Button(edit_manu,bg='#F7FFE3', font=("Cooper Black", 17), fg="#000000", text="ADD",command=add)
        add_button.place(x=600, y=120, width=250, height=64)

        edit_button = tk.Button(edit_manu, bg="#F7FFE3", font=("Cooper Black", 17), fg="#000000", text="EDIT",command=edit)
        edit_button.place(x=600, y=210, width=250, height=64)
        
        delete_button = tk.Button(edit_manu, bg="#F7FFE3", font=("Cooper Black", 17), fg="#000000", text="DELETE",command=delete)
        delete_button.place(x=600, y=300, width=250, height=64)

        editmanu_label = tk.Label(edit_manu, bg="#000000", font=("Tahoma", 13), fg="#ffffff", justify="center",borderwidth="1px", text="ชื่อสินค้า", relief="sunken")
        editmanu_label.place(x=300, y=140, width=140, height=30)

        priceman_label = tk.Label(edit_manu, bg="#000000", font=("Tahoma", 13), fg="#ffffff", justify="center",borderwidth="1px", text="ราคาสินค้า", relief="sunken")
        priceman_label.place(x=300, y=250, width=140, height=30)


        products_listbox = tk.Listbox(edit_manu, bg="#ffffff", borderwidth="4px", font=("Tahoma", 14), fg="#333333", relief="sunken")
        products_listbox.place(x=70, y=400, width=840, height=220)

        end = tk.Button(edit_manu, bg="#76b666", font=("Tahoma", 20), justify="center", text="🔙", borderwidth="3px",command=root, highlightthickness=0, bd=0)
        end.place(x=9, y=8, width=40, height=40)
        
        def back():
            edit_manu.withdraw()
            root.deiconify()
        end = tk.Button(edit_manu, bg="#76b666", font=("Tahoma", 15), justify="center", text="🔙", borderwidth="3px",command=back, highlightthickness=0, bd=0)
        end.place(x=9, y=8, width=40, height=40)
        

        login_window.destroy()
        
    def login_window():
        global root
    root.withdraw()



    login_window = tk.Toplevel(root)
    login_window.title("ล็อกอิน")
    login_window.geometry('500x500+350+200')
    login_window.resizable(False, False)
    img = Image.open(r'c:\Users\Thirawat\Downloads\claim your freebie instagram notification engagement post .png')
    img = img.resize((500, 500))
    photo = ImageTk.PhotoImage(img)
    img_label1 = Label(login_window, image=photo)
    img_label1.photo = photo 
    img_label1.place(x=0,y=0)
    
    # สร้าง Label และ Entry สำหรับชื่อผู้ใช้งานและรหัสผ่าน
    username_entry = ttk.Entry(login_window,width=20)
    username_entry.place(x=245,y=205)
    username_entry.config(background='#E09B80')
    password_entry = ttk.Entry(login_window,width=20, show="*")  # ใส่ show="*" เพื่อซ่อนรหัสผ่าน
    password_entry.place(x=245,y=280)
    
    # สร้างปุ่มเพื่อเรียกใช้งานฟังก์ชัน login
    login_button = ttk.Button(login_window, text="เข้าสู่ระบบ", command=edit_manu,width=15)
    login_button.place(x=200,y=338)
    login_window.mainloop()



def Backyard():
    
        
    def Summary():
        global summary
        summary = tk.Toplevel()
        summary.title("สรุปยอดขาย")
        summary.geometry("1285x760+125+15")

        # เปิดรูปภาพ
        image = Image.open(r'c:\Users\Thirawat\Downloads\CUSTOMER (5).png')
        # ปรับขนาดรูปภาพ
        new_width = 1285  # กว้างใหม่ของรูปภาพ
        new_height = 760  # สูงใหม่ของรูปภาพ
        resized_image = image.resize((new_width, new_height))
        # สร้าง PhotoImage จากรูปภาพที่ปรับขนาดแล้ว
        photo = ImageTk.PhotoImage(resized_image)
        label = tk.Label(summary, image=photo)
        label.image = photo  
        label.place(x=0,y=0)

        
        summary.option_add("*Font", "Tahoma 25")
    Summary()
    def SummaryDay():
            connection = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
            cursor = connection.cursor()
            # ดึงข้อมูลการขายจากฐานข้อมูล
            cursor.execute("SELECT date, SUM(price) FROM bill GROUP BY date")
            results = cursor.fetchall() 
            style = ttk.Style()
            style.configure("Treeview", font=("Tahoma", 20)) 
            style.configure("Treeview.Heading", font=("Tahoma", 20))
            
            for row in result_tree.get_children():
                result_tree.delete(row)
            # แสดงผลลัพธ์ในตาราง
            for date, price in results:
                total_with_baht = f"{price} บาท"
                result_tree.insert("", "end", values=(date, total_with_baht))

    def SummaryMonth():
            connection = sqlite3.connect(r"c:\Users\Thirawat\Desktop\[u,\py\newprojectgood.db")
            cursor = connection.cursor()
            # ดึงข้อมูลการขายจากฐานข้อมูล
            # เปลี่ยน SQL Query เพื่อรวมยอดขายรายเดือน
            cursor.execute("SELECT month, SUM(price) FROM bill GROUP BY month")
            results = cursor.fetchall() 
            style = ttk.Style()
            style.configure("Treeview", font=("Tahoma", 20)) 
            style.configure("Treeview.Heading", font=("Tahoma", 20))
            for row in result_tree.get_children():
                result_tree.delete(row)
            # แสดงผลลัพธ์ในตาราง
            for month, price in results:
                total_with_baht = f"{price} บาท"
                result_tree.insert("", "end", values=(month, total_with_baht))
    result_tree = ttk.Treeview(summary, columns=("Date", "Total"),height=20)
    result_tree.heading("#1", text="วันที่")
    result_tree.heading("#2", text="ยอดรวม")
    result_tree.place(x=350,y=100)
    vertical_scrollbar = ttk.Scrollbar(summary, orient="vertical", command=result_tree.yview)
    # เชื่อมตาราง Treeview กับ Scrollbar
    result_tree.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.place(x=610,y=1000)
        
    def closedelete():
            summary.destroy()
            
    Button(summary,text="รายวัน",font=("Tahoma",23,"bold"),borderwidth = 0,width=10,bg='#1F798A',fg='#FFFFB0',activebackground = "#1F798A",command=SummaryDay).place(x=750,y=673)
    Button(summary,text="รายเดือน",font=("Tahoma",23,"bold"),borderwidth = 0,width=10,bg='#1F798A',fg='#FFFFB0',activebackground = "#1F798A",command=SummaryMonth).place(x=1040,y=673)
    Button(summary,text="<-- ย้อนกลับ",font=("Tahoma",23,"bold"),borderwidth = 0,width=15,bg='#1F798A',fg='#FFFFB0',activebackground = "#1F798A",command=closedelete).place(x=95,y=668)
    summary.mainloop()

    
root = Tk()
root.title('เมนูหลัก')
root.geometry('1020x665+200+100')
root.resizable(False, False)
img = Image.open(r'c:\Users\Thirawat\Downloads\CUSTOMER (5).png')
img = img.resize((1020,665))
photo = ImageTk.PhotoImage(img)
img_label = tk.Label(root, image=photo)
img_label.pack()

# Create buttons for the main window หลังร้าน
btn_img = Image.open(r'c:\Users\Thirawat\Downloads\new new new new new new (1).png') 
btn_img = btn_img.resize((230, 230))
btn_photo = ImageTk.PhotoImage(btn_img)
btn1 = Button(root, image=btn_photo, command=Backyard) 
btn1.photo = btn_photo
btn1.place(x=50, y=140)

btn_img1 = Image.open(r'c:\Users\Thirawat\Downloads\new new new new new new (2).png')
btn_img1 = btn_img1.resize((230, 230))
btn_photo1 = ImageTk.PhotoImage(btn_img1)
btn2 = Button(root, image=btn_photo1, command=open_menushow)
btn2.photo = btn_photo1
btn2.place(x=680, y=140)

btn_img2 = Image.open(r'c:\Users\Thirawat\Downloads\new new new new new new.png')
btn_img2 = btn_img2.resize((230, 230))
btn_photo2 = ImageTk.PhotoImage(btn_img2)
btn3 = Button(root, image=btn_photo2, command=show_developer_info)
btn3.photo = btn_photo2
btn3.place(x=345, y=140)

btn_img3 = Image.open(r'c:\Users\Thirawat\Downloads\แก้ไข (1).png')
btn_img3 = btn_img3.resize((230, 230))
btn_photo3 = ImageTk.PhotoImage(btn_img3)
btn3 = Button(root, image=btn_photo3, command=show_edit)
btn3.photo = btn_photo3
btn3.place(x=205, y=405)

root.mainloop()

