import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image, ImageTk




#To set connection with sqlite3 Railway.db

def connection():
    con=sqlite3.connect('Railway.db')
    cursor=con.cursor()
    return con,cursor




#Login function gets triggred on pressing LOGIN button

def login():
    if not e_u.get().isnumeric():
        e_u.set("")
        e_p.set("")
        msg.showerror('ERROR','Incorrect Userid/Password!')
    else:    
        id=int(e_u.get())
        pwd=e_p.get()
        e_u.set("")
        e_p.set("")
        con,cur=connection()
        cur.execute("select * from ticket where ticket_id={} and user_password='{}'".format(id,pwd))
        result=cur.fetchall()
        
        if result!=[]:
            for i in result:
                #i=(101, '101@IRCTC', 12674, 'CHERAN EXPRESS', 'CBE', 'COIMBATORE JUNCTION', 'MAS', 'MGR CHENNAI CENTRAL', '01-01-22', '22-40', 2, 290)
                ticket_id=i[0]
                if id!='' and pwd!='':
                    msg.showinfo("",'Login sucessful')
                    login_screen.destroy()  
                    personal_details(ticket_id)
        else:
            msg.showerror('ERROR','Incorrect Userid/Password!')
    con.close()
    
    


#window to display Personal details of the passenger based on the Ticket ID

def personal_details(ticket_id):
    info = Tk()
    info.geometry('1170x300')
    info.title('Details')
    info.iconbitmap('assets\Logo.ico')
    title_label = Label(info,text="Ticket Infomation",font=("Calibri bold", 18))
    title_label.pack(pady=10)

    table_frame=Frame(info).pack(padx=50,pady=20)
    tree=ttk.Treeview(table_frame,height=3)
    
    tree["columns"]=("1","2","3","4","5","6","7","8","9","10")
    
    tree.column("#0", width=120, minwidth=110, stretch=NO,anchor=CENTER)
    tree.column("1", width=50, minwidth=50, stretch=NO,anchor=CENTER)
    tree.column("2", width=50, minwidth=50,stretch=NO,anchor=CENTER)
    tree.column("3", width=130, minwidth=100, stretch=NO,anchor=CENTER)
    tree.column("4", width=210, minwidth=170, stretch=NO,anchor=CENTER)
    tree.column("5", width=160, minwidth=100, stretch=NO,anchor=CENTER)
    tree.column("6", width=150, minwidth=100, stretch=NO,anchor=CENTER)
    tree.column("7", width=100, minwidth=80, stretch=NO,anchor=CENTER)
    tree.column("8", width=100, minwidth=80, stretch=NO,anchor=CENTER)
    tree.column("9", width=100, minwidth=80, stretch=NO,anchor=CENTER)
    
    tree.heading("#0",text="PASSENGER_NAME")
    tree.heading("1", text="AGE")
    tree.heading("2", text="SEX")
    tree.heading("3", text="DATE_OF_BIRTH")
    tree.heading("4", text="TRAIN_NAME")
    tree.heading("5", text="ORIGIN")
    tree.heading("6", text="DESTINATION")
    tree.heading("7", text="TRAVEL_DATE")
    tree.heading("8", text="DEPARTURE_TIME")
    tree.heading("9", text="FARE_PER_HEAD")
    
    tree.pack(fill=X)

    btnFrame = Frame(info)
    schedule_button=ttk.Button(btnFrame,text="    TICKET SCHEDULE    ",takefocus=False, command=lambda: schedule(info))
    schedule_button.pack(pady=30,side=BOTTOM)
    btnFrame.pack(fill=X)

    # inserting values to tree
    con, cur = connection()
    lst = cur.execute("select PASSENGER_NAME,AGE,SEX,DATE_OF_BIRTH,TRAIN_NAME,STATION_NAME,DESTINATION,TRAVEL_DATE,TRAVEL_TIME,TOTAL_FARE,HEAD_COUNT from PASSENGER_DETAILS natural join TICKET where TICKET_ID={}".format(ticket_id))
    
    for tup in lst:
        d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10=tup
        tree.insert("", "end", text=str(d0), values=(str(d1), str(d2), str(d3), str(d4), str(d5),str(d6),str(d7),str(d8),str(d9/d10)))
    
    tk.Label(info,text='Cost of Trip:  {}'.format(d9),relief=RIDGE).place(width=150,height=30,x=1000,y=200)
    con.close()





#schedule window to display the weekly schedule of the Trains

def schedule(win):
    win.destroy()
    schedule = Tk()
    schedule.geometry('870x400')
    schedule.title('Ticket Schedule')
    schedule.iconbitmap('assets\Logo.ico')
    title_label = Label(schedule,text='Weekly Schedule',font=("Calibri bold", 17))
    title_label.pack(pady=10)

    table_frame = Frame(schedule)
    table_frame.pack()
    sb = ttk.Scrollbar(table_frame)  
    tree=ttk.Treeview(table_frame, height=9,yscrollcommand = sb.set)
    tree["columns"]=("1","2","3","4","5","6")
    
    tree.column("1", width=90, minwidth=100, stretch=NO,anchor=CENTER)
    tree.column("#0", width=190, minwidth=120, stretch=NO,anchor=CENTER)
    tree.column("2", width=140, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("3", width=130, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("4", width=100, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("5", width=100, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("6", width=100, minwidth=100,stretch=NO,anchor=CENTER)
    
    tree.heading("#0",text="TRAIN_NAME")
    tree.heading("1", text="TRAIN_ID")
    tree.heading("2", text="STARTING_STATION")
    tree.heading("3", text="ENDING_STATION")
    tree.heading("4", text="TRAVEL_TIME")
    tree.heading("5", text="DISTANCE_IN_KMS")
    tree.heading("6", text="STOPS_NOS")

    sb.config(command = tree.yview)
    sb.pack(side = RIGHT, fill=Y)
    tree.pack(fill=X)
    
    btnFrame = Frame(schedule)
    ttk.Button(btnFrame,text="STATIONS PASSING",takefocus=False, command=lambda: station_details(tree)).pack(pady=8)#height=50,width=120,x=100,y=320
    ttk.Button(btnFrame,text="TRAIN DESCRIPTION",takefocus=False,command=lambda: train_desc(tree)).pack(pady=8)#side=BOTTOM
    ttk.Button(btnFrame,text="TICKET AVAILABILITY",takefocus=False,command=lambda: ticket_availability(tree)).pack(pady=8)#padx=20,pady=10,side=RIGHT
    btnFrame.pack(fill=X)

    # inserting values to tree
    con, cur = connection()
    lst = cur.execute("select TRAIN_NAME,TRAIN_ID,STARTING_STATION,ENDING_STATION,TRAVEL_TIME,DISTANCE_IN_KMS,STOPS from TRAIN_ROUTE")
    for tup in lst:
            d0,d1,d2,d3,d4,d5,d6=tup
            tree.insert("", "end", text=d0, values=(str(d1), str(d2), str(d3), str(d4), str(d5),str(d6)))
    con.commit()
    con.close()





#Station_details to display the stations a selected train passes through based on it ID

def station_details(tree):
    train_id=tree.item(tree.selection())['values'][0]
    stations=Toplevel()
    stations.geometry('700x300')
    stations.iconbitmap('assets\Logo.ico')
    stations.title('Stations')
    stations.config(bg='#4DC1A2')
    con,curr = connection()
    curr.execute('SELECT TRAIN_NAME FROM TRAIN WHERE TRAIN_ID={}'.format(train_id))
    value=curr.fetchall()
    title_label = Label(stations,text='{} PASSES THROUGH THE STATIONS'.format(value[0][0]),font=("Calibri bold", 17),bg='#4DC1A2')
    title_label.pack(pady=10)
    curr.close()
    
    table_frame = Frame(stations)
    table_frame.pack()
    
    sb = ttk.Scrollbar(table_frame)  
    tree=ttk.Treeview(table_frame, height=7,yscrollcommand = sb.set)
    tree["columns"]=("1","2","3","4")
    
    tree.column("#0", width=190, minwidth=120, stretch=NO,anchor=CENTER)
    tree.column("1", width=90, minwidth=100, stretch=NO,anchor=CENTER)
    tree.column("2", width=140, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("3", width=130, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("4", width=100, minwidth=100,stretch=NO,anchor=CENTER)
    
    tree.heading("#0",text="STATION_NAME")
    tree.heading("1", text="ARRIVAL")
    tree.heading("2", text="DEPARTURE")
    tree.heading("3", text="HALT_TIME")
    tree.heading("4", text="RUNNING_DAY")

    sb.config(command = tree.yview)
    sb.pack(side = RIGHT, fill=Y)
    tree.pack(fill=X)
    
    con, cur = connection()
    lst = cur.execute("select STATION_NAME,ARRIVAL,DEPARTURE,HALT_TIME,RUNNING_DAY from TRAIN_JOURNEY where TRAIN_ID={} order by RUNNING_DAY,departure".format(train_id))
    for tup in lst:
            d0,d1,d2,d3,d4=tup
            tree.insert("", "end", text=d0, values=(str(d1), str(d2), str(d3), str(d4)))
    
    con.commit()
    con.close()

    


#Train_desc to display the description of a selected train based on its ID
    
def train_desc(tree):
    train_id=tree.item(tree.selection())['values'][0]
    description=Toplevel()
    description.geometry('750x150')
    description.iconbitmap('assets\Logo.ico')
    description.title('Stations')
    description.config(bg='#9F94BF')
    con,curr = connection()
    curr.execute('SELECT TRAIN_NAME FROM TRAIN WHERE TRAIN_ID={}'.format(train_id))
    value=curr.fetchall()
    title_label = Label(description,text='DESCRIPTION OF {}'.format(value[0][0]),font=("Calibri bold", 17),bg='#9F94BF')
    title_label.pack(pady=10)
    curr.close()
    
    table_frame = Frame(description)
    table_frame.pack()
    
    tree=ttk.Treeview(table_frame, height=1)
    tree["columns"]=("1","2","3","4")
    
    tree.column("#0", width=190, minwidth=140, stretch=NO,anchor=CENTER)
    tree.column("1", width=150, minwidth=100, stretch=NO,anchor=CENTER)
    tree.column("2", width=140, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("3", width=130, minwidth=100,stretch=NO,anchor=CENTER)
    tree.column("4", width=100, minwidth=100,stretch=NO,anchor=CENTER)
    
    tree.heading("#0",text="TRAIN_NAME")
    tree.heading("1", text="TRAIN_TYPE")
    tree.heading("2", text="RUN_DAYS")
    tree.heading("3", text="TOTAL_CAPACITY")
    tree.heading("4", text="COST_PER_SEAT")
    tree.pack(fill=X)
    
    con, cur = connection()
    lst = cur.execute("select TRAIN_NAME,TRAIN_TYPE,RUN_DAYS,CAPACITY,COST_PER_SEAT from train where TRAIN_ID={}".format(train_id))
    for tup in lst:
            d0,d1,d2,d3,d4=tup
            tree.insert("", "end", text=d0, values=(str(d1), str(d2), str(d3), str(d4)))
    
    con.commit()
    con.close()
    
    
    

#ticket_availability to display the availability of tickets in a selected train

def ticket_availability(tree):
    train_id=tree.item(tree.selection())['values'][0]
    con,cur=connection()
    cur.execute('select capacity-(select sum(head_count) as total_passengers from ticket group by train_id having train_id={}) from train where train_id={}'.format(train_id,train_id))
    res=cur.fetchall()
    msg.showinfo('Ticket availability','Available tickets\n      {}'.format(res[0][0]))




#LOGIN SCREEN
#__main__:
login_screen=Tk()
login_screen.geometry('800x660')
login_screen.title('Railways')
login_screen.iconbitmap('assets\Logo.ico')
login_screen.configure(bg='grey')
s = ttk.Style()
s.configure('TButton', font=('Calibri', 24))
s.configure("Treeview.Heading", font=('Calibri', 14))
s.configure('Treeview', rowheight=27, font=('Calibri', 12))


img= (Image.open("assets\IRCTC.png"))
resized_image= img.resize((300,200), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)
canvas= Canvas(login_screen, width= 500, height= 200)
canvas.create_image(0,0, anchor=NW, image=new_image)
canvas.pack(padx = 250, pady= 50)

f1=Frame(login_screen,bd=5,relief=RAISED) #must be flat, groove, raised, ridge, solid, or sunken
f1.pack()

f2=Frame(login_screen,bd=1,relief=SUNKEN)
f2.pack(fill=X,padx = 32, pady = 20)
names_frame = Frame(f2)
names_frame.pack(pady = 10)
Label(names_frame,text="Made by: ",font=("Consolas",12,'italic')).pack(side=LEFT)
Label(names_frame,text="H Abdurrahman Lalsudhesh",font=("Consolas",11,'italic')).pack(side=LEFT, padx= 40)
Label(names_frame,text="Aruneeswaran K",font=("Consolas",11,'italic')).pack(side=LEFT, padx = 40)
Label(names_frame,text="Jiitesh S",font=("Consolas",11,'italic')).pack(side=LEFT, padx = 40)

label_userid=tk.Label(login_screen,text='User ID:',justify=LEFT).place(width=70,height=25,x=294,y=350)
label_password=tk.Label(login_screen,text='Password:').place(width=70,height=25,x=300,y=380)

e_u=tk.StringVar()
e_p=tk.StringVar()
entry_userid=tk.Entry(login_screen,textvariable=e_u).place(width=100,height=25,x=370,y=350)
entry_password=tk.Entry(login_screen,show='*',textvariable=e_p).place(width=100,height=25,x=370,y=380)

border2 = Frame(f1)
login_button=ttk.Button(border2,text="login",style="W.TButton",width=10,takefocus=False, command=login)
login_button.pack(pady=20,side=BOTTOM)
border2.pack(padx=70,pady=90)

login_screen.mainloop()
