# MySQL GUI by Tera
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
import pickle
import pymysql
from tkinter import ttk



# part1: software login ###################
# software welcome window
window = tk.Tk()
window.title('Welcome to MySQL')
window.geometry('450x300')
window.resizable(width = False, height = False)

# welcome image
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = canvas.create_image(225, 0, anchor='n', image=image_file)
canvas.pack(side='top')

# user information
tk.Label(window, text='Username: ').place(x=50, y= 150)
tk.Label(window, text='Password: ').place(x=50, y= 190)

var_usr_name = tk.StringVar()
var_usr_name.set('example@mysql.com')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)


def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
            window.destroy()
        else:
            tk.messagebox.showerror(message='Error, your password is wrong, try again.')
    else:
        is_sign_up = tk.messagebox.askyesno('Welcome',
                               'You have not signed up yet. Sign up today?')
        if is_sign_up:
            usr_sign_up()


def usr_sign_up():
    def sign_to_mysql():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if np != npf:
            tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('Error', 'The user has already signed up!')
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            window_sign_up.destroy()
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    new_name.set('example@python.com')
    tk.Label(window_sign_up, text='Username: ').place(x=10, y= 10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y= 90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_mysql)
    btn_comfirm_sign_up.place(x=150, y=130)


# login and sign up button
btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=170, y=230)
btn_sign_up = tk.Button(window, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=270, y=230)

window.mainloop()

# part2: mysql login #####################
# login window
window1 = tk.Tk()
window1.title('Connect to MySQL')
window1.geometry('300x500')
window1.config(bg='#FDFDFD')
window1.resizable(width = False, height = False)

# mysql image
c1 = tk.Canvas(window1, height=100, width=300, bg='#FDFDFD')
image_file1 = tk.PhotoImage(file='mysql.gif')
image1 = c1.create_image(150, 50, anchor='center', image=image_file1)
c1.pack(side='top')

# mysql user information
dy = 15
tk.Label(window1, text='        host: ', bg='#FDFDFD').place(x=20, y=150+dy)
tk.Label(window1, text='        user: ', bg='#FDFDFD').place(x=20, y=190+dy)
tk.Label(window1, text='password: ', bg='#FDFDFD').place(x=20, y=230+dy)
tk.Label(window1, text='  dbname: ', bg='#FDFDFD').place(x=20, y=270+dy)
tk.Label(window1, text='        port: ', bg='#FDFDFD').place(x=20, y=310+dy)

var_usr_host1 = tk.StringVar()
var_usr_name1 = tk.StringVar()
var_usr_pwd1 = tk.StringVar()
var_usr_dbn1 = tk.StringVar()
var_usr_port1 = tk.StringVar()
entry_usr_host1 = tk.Entry(window1, textvariable=var_usr_host1, bg='GhostWhite')
entry_usr_name1 = tk.Entry(window1, textvariable=var_usr_name1, bg='GhostWhite')
entry_usr_pwd1 = tk.Entry(window1, textvariable=var_usr_pwd1, show='*', bg='GhostWhite')
entry_usr_dbn1 = tk.Entry(window1, textvariable=var_usr_dbn1, bg='GhostWhite')
entry_usr_port1 = tk.Entry(window1, textvariable=var_usr_port1, bg='GhostWhite')
entry_usr_host1.place(x=110, y=150+dy)
entry_usr_name1.place(x=110, y=190+dy)
entry_usr_pwd1.place(x=110, y=230+dy)
entry_usr_dbn1.place(x=110, y=270+dy)
entry_usr_port1.place(x=110, y=310+dy)

# mysql log in button

def mysqllog():
    vhost = var_usr_host1.get()
    vname = var_usr_name1.get()
    vpwd = var_usr_pwd1.get()
    vdbn = var_usr_dbn1.get()
    vport = var_usr_port1.get()

    try:
        conn = pymysql.Connect(
            host=vhost,
            port=int(vport),
            user=vname,
            passwd=vpwd,
            db=vdbn,
            charset='utf8'
            )
    except:
        tk.messagebox.showerror(title='Error', message='Login failed!\nPlease try again.')
    else:
        tk.messagebox.showinfo(title='Information', message='Login succeeded!')
        conn.close()    # close the connection
        window1.destroy()


btn_mysqllog = tk.Button(window1, text='Login', command=mysqllog)
btn_mysqllog.place(x=150, y=430, anchor='center')

window1.mainloop()


# part3: main window ############################
# window2
window2 = tk.Tk()
window2.title('MySQL GUI')
window2.geometry('1024x768')


# frames

frm1=tk.Frame(window2, width=768, height=512)
frm1.place(x=0, y=0, anchor='nw')
frm2=tk.Frame(window2, width=256, height=512)
frm2.place(x=768, y=0, anchor='nw')
frm3=tk.Frame(window2, width=768, height=256)
frm3.place(x=0, y=513, anchor='nw')
frm4=tk.Frame(window2, width=256, height=256)
frm4.place(x=768, y=512, anchor='nw')

# ctest1 = tk.Canvas(frm1, bg='blue', width=768, height=512).pack()
# ctest2 = tk.Canvas(frm2, bg='green', width=256, height=512).pack()
# ctest3 = tk.Canvas(frm3, bg='yellow', width=768, height=256).pack()
# ctest4 = tk.Canvas(frm4, bg='red', width=256, height=256).pack()

# frame 1


tree = ttk.Treeview(frm1, height=512,  show="headings")
tree["columns"] = ("StuNo", "StuName", "StuSex", "Class", "Department")
tree.column("StuNo", width=154, anchor="center")
tree.column("StuName", width=153, anchor="center")
tree.column("StuSex", width=154, anchor="center")
tree.column("Class", width=153, anchor="center")
tree.column("Department", width=154, anchor="center")

tree.heading("StuNo", text="StuNo")
tree.heading("StuName", text="StuName")
tree.heading("StuSex", text="StuSex")
tree.heading("Class", text="Class")
tree.heading("Department", text="Department")

tree.pack()


def delete_tree():
    items = tree.get_children()
    for item in items:
        tree.delete(item)


# frame2

c_background = tk.Canvas(window2, width=176, height=91)
image_file12 = tk.PhotoImage(file='mysql.gif')
image12 = c_background.create_image(0, 0, anchor='nw', image=image_file12)
c_background.place(x=768, y=513, anchor='se')

btn_change=tk.Button(frm2, text='Books', width=10, height=2).place(x=43, y=100, anchor='nw')
var_r_stuno = tk.IntVar()
var_r_stuname = tk.IntVar()
var_r_class = tk.IntVar()


def lookup():
    no = v_fr3_stuno.get()
    name = v_fr3_stuname.get()
    stuclass = v_fr3_class.get()
    a1 = var_r_stuno.get()
    a2 = var_r_stuname.get()
    a3 = var_r_class.get()

    if a1 == 1 and a2 == 0 and a3 == 0:
        db = pymysql.connect(host="localhost", user="root", password="lzy19980324xyz", db="library", port=3306)
        cur = db.cursor()
        sql = "select * from student where StuNo='%s'" % no
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                result_stuno = row[0]
                result_stuname = row[1]
                result_stusex = row[2]
                result_class = row[3]
                relust_department = row[4]

                delete_tree()
                tree.insert("", 0, text='data1', values=(result_stuno, result_stuname, result_stusex, result_class, relust_department))

        except Exception as e:
            raise e
        finally:
            db.close()

    if a1 == 0 and a2 == 1 and a3 == 0:
        db = pymysql.connect(host="localhost", user="root", password="lzy19980324xyz", db="library", port=3306)
        cur = db.cursor()
        sql = "select * from student where StuName='%s'" % name
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                result_stuno = row[0]
                result_stuname = row[1]
                result_stusex = row[2]
                result_class = row[3]
                relust_department = row[4]
                delete_tree()
                tree.insert("", 0, text='data1',
                            values=(result_stuno, result_stuname, result_stusex, result_class, relust_department))

        except Exception as e:
            raise e
        finally:
            db.close()

    if a1 == 0 and a2 == 1 and a3 == 0:
        db = pymysql.connect(host="localhost", user="root", password="lzy19980324xyz", db="library", port=3306)
        cur = db.cursor()
        sql = "select * from student where Class='%s'" % stuclass
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                result_stuno = row[0]
                result_stuname = row[1]
                result_stusex = row[2]
                result_class = row[3]
                relust_department = row[4]
                delete_tree()
                tree.insert("", 0, text='data1',
                            values=(result_stuno, result_stuname, result_stusex, result_class, relust_department))

        except Exception as e:
            raise e
        finally:
            db.close()
    else:
        tk.messagebox.showerror(title='Error',message='QueryError!')


rbtn_stuno = tk.Checkbutton(frm2, width=10, height=2, text='StuNo    ', variable=var_r_stuno, onvalue=1, offvalue=0
                            , font=('Arial', 20)).place(x=43, y=76, anchor='nw')
rbtn_stuname = tk.Checkbutton(frm2, width=10, height=2, text='StuName', variable=var_r_stuname, onvalue=1, offvalue=0
                              , font=('Arial', 20)).place(x=43, y=166, anchor='nw')
rbtn_class = tk.Checkbutton(frm2, width=10, height=2, text='Class     ', variable=var_r_class, onvalue=1, offvalue=0
                            , font=('Arial', 20)).place(x=43, y=256, anchor='nw')
btn_select = tk.Button(frm2, width=10, height=2, text='Lookup'
                       , font=('Arial', 20), command=lookup).place(x=43, y=346, anchor='nw')

# frame3

idx = 70
l_fr3_stuno = tk.Label(frm3, text='StuNo:', width=10, height=1, font=('Arial', 20)).place(x=384-idx, y=35, anchor='ne')  # 160*37
l_fr3_stuname= tk.Label(frm3, text='StuName:', width=10, height=1, font=('Arial', 20)).place(x=384-idx, y=72, anchor='ne')
l_fr3_stusex= tk.Label(frm3, text='StuSex:', width=10, height=1, font=('Arial', 20)).place(x=384-idx, y=109, anchor='ne')
l_fr3_class= tk.Label(frm3, text='Class:', width=10, height=1, font=('Arial', 20)).place(x=384-idx, y=146, anchor='ne')
l_fr3_department= tk.Label(frm3, text='Department:', width=10, height=1, font=('Arial', 20)).place(x=384-idx, y=183, anchor='ne')

v_fr3_stuno = tk.StringVar()
v_fr3_stuname = tk.StringVar()
v_fr3_stusex = tk.StringVar()
v_fr3_class = tk.StringVar()
v_fr3_department = tk.StringVar()

e_fr3_stuno = tk.Entry(frm3, font=('Arial', 20), textvariable=v_fr3_stuno).place(x=384-idx, y=35, anchor='nw')
e_fr3_stuname = tk.Entry(frm3, font=('Arial', 20), textvariable=v_fr3_stuname).place(x=384-idx, y=72, anchor='nw')
e_fr3_stusex = tk.Entry(frm3, font=('Arial', 20), textvariable=v_fr3_stusex).place(x=384-idx, y=109, anchor='nw')
e_fr3_class = tk.Entry(frm3, font=('Arial', 20), textvariable=v_fr3_class).place(x=384-idx, y=146, anchor='nw')
e_fr3_department = tk.Entry(frm3, font=('Arial', 20), textvariable=v_fr3_department).place(x=384-idx, y=183, anchor='nw')

# frame4


def set_empty():
    v_fr3_stuno.set('')
    v_fr3_stuname.set('')
    v_fr3_stusex.set('')
    v_fr3_class.set('')
    v_fr3_department.set('')


def insert():
    no = v_fr3_stuno.get()
    name = v_fr3_stuname.get()
    sex = v_fr3_stusex.get()
    stuclass = v_fr3_class.get()
    department = v_fr3_department.get()
    db = pymysql.connect(host="localhost", user="root",password="lzy19980324xyz", db="library", port=3306)
    cur = db.cursor()
    sql_insert = r"insert into student(StuNo,StuName,StuSex,Class,Department) values('%s','%s','%s','%s','%s')" % (no, name, sex, stuclass, department)
    try:
        cur.execute(sql_insert)
        db.commit()
        tk.messagebox.showinfo(title='Insert', message='Insert Succeeded!')
        set_empty()
    except:
        db.rollback()
        tk.messagebox.showerror(title='Insert', message='Insert Failed!')
        set_empty()
    finally:
        db.close()


def update():
    no = v_fr3_stuno.get()
    name = v_fr3_stuname.get()
    sex = v_fr3_stusex.get()
    stuclass = v_fr3_class.get()
    department = v_fr3_department.get()
    # delete
    db = pymysql.connect(host="localhost", user="root", password="lzy19980324xyz", db="library", port=3306)
    cur = db.cursor()
    sql_delete = "delete from student where StuNo='%s'" % no

    try:
        cur.execute(sql_delete)
        db.commit()
    except:
        db.rollback()
        tk.messagebox.showerror(title='Update', message='Update Failed!')
    finally:
        db.close()
    # insert
    db = pymysql.connect(host="localhost", user="root", password="lzy19980324xyz", db="library", port=3306)
    cur = db.cursor()
    sql_insert = r"insert into student(StuNo,StuName,StuSex,Class,Department) values('%s','%s','%s','%s','%s')" % (
    no, name, sex, stuclass, department)
    try:
        cur.execute(sql_insert)
        db.commit()
        tk.messagebox.showinfo(title='Update', message='Update Succeeded!')
        set_empty()
    except:
        db.rollback()
        tk.messagebox.showerror(title='Update', message='Update Failed!')
        set_empty()
    finally:
        db.close()


def delete():
    no = v_fr3_stuno.get()
    name = v_fr3_stuname.get()
    sex = v_fr3_stusex.get()
    stuclass = v_fr3_class.get()
    department = v_fr3_department.get()
    db = pymysql.connect(host="localhost", user="root", password="lzy19980324xyz", db="library", port=3306)
    cur = db.cursor()
    sql_delete = "delete from student where StuNo='%s' or StuName='%s' or StuSex='%s' or Class='%s' or Department='%s'" % (no, name, sex, stuclass, department)

    try:
        cur.execute(sql_delete)
        db.commit()
        delete_tree()
        tk.messagebox.showinfo(title='Delete', message='Delete Succeeded!')
        set_empty()
    except:
        db.rollback()
        tk.messagebox.showerror(title='Delete', message='Delete Failed!')
        set_empty()
    finally:
        db.close()


def quit():
    a = tk.messagebox.askyesno(title='Information', message='Are you sure to exit?')
    if a:
        window2.quit()


idy = 12
btn_insert = tk.Button(frm4, width=10, height=1, text='Insert', font=('Arial', 15)
                       , command=insert).place(x=68, y=8+idy, anchor='nw') # 120*60
btn_update = tk.Button(frm4, width=10, height=1, text='Update', font=('Arial', 15)
                       , command=update).place(x=68, y=68+idy, anchor='nw')
btn_delete = tk.Button(frm4, width=10, height=1, text='Delete', font=('Arial', 15)
                       , command=delete).place(x=68, y=128+idy, anchor='nw')
btn_quit = tk.Button(frm4, width=10, height=1, text='Quit', font=('Arial', 15)
                     , command=quit).place(x=68, y=188+idy, anchor='nw')

window2.mainloop()



