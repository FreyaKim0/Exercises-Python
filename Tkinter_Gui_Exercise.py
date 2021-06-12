import tkinter as tk
from tkinter import ttk
from tkinter.constants import NORMAL
from tkinter import messagebox as mb

# On click Method
def reset():
    FullNameInput.delete(0,'end')
    FullNameInput.insert(0,FullNameInput.defaultValue)
    ResidencyS.set("Domestic")
    ProgramC.delete(0,'end')
    ProgramC.current(2)
    programVar.set(1)
    WebVar.set(0)
    softwareVar.set(0)

def okay():
    fullname = FullNameInput.get()
    status = ResidencyS.get()
    programs = ProgramC.get()
    courseS =""

    if(programVar.get()==1):
        courseS+='Programming1\n'
    if(WebVar.get()==1):
        courseS+='Web Page Design\n'
    if(softwareVar.get()==1):
        courseS+='software Engineering\n'
    
    mb.showinfo('Information','Fullname: %s\nResidency: %s\nProgram: %s\nCourse: \n%s'%(fullname,status,programs,courseS))

def exit():
    window.destroy()

# Create the Tkinter window.
window = tk.Tk()
window.title("Centennial College")
window.minsize(350,360)

# Create a division with the help of Frame class and align them on TOP and BOTTOM with pack() method.
top_frame = tk.Frame(master=window, height=50, bg="#9B90C2")
top_frame.pack(fill=tk.X)

center_frame = tk.Frame(master=window)
center_frame.pack(fill=tk.X,expand=tk.YES)

btm_frame = tk.Frame(master=window, height=60, bg="#9B90C2")
btm_frame.pack(fill=tk.X)

# Center left and right columns
center_frame1 = tk.Frame(center_frame,width=25, height=250)
center_frame1.pack(fill=tk.X,side=tk.LEFT,expand=True)

center_frame2 = tk.Frame(center_frame,width=150, height=250)
center_frame2.pack(fill=tk.X,side=tk.LEFT,expand=True)

# Bottom 3 columns
btm_frame1 = tk.Frame(btm_frame,width=66, height=60, bg="#622954")
btm_frame1.pack(fill=tk.X,side=tk.LEFT,expand=True)

btm_frame2 = tk.Frame(btm_frame,width=67, height=60, bg="#66327C")
btm_frame2.pack(fill=tk.X,side=tk.LEFT,expand=True)

btm_frame3 = tk.Frame(btm_frame,width=67, height=60, bg="#8A6BBE")
btm_frame3.pack(fill=tk.X,side=tk.LEFT,expand=True)

# Title
title = tk.Label(top_frame,text='ICET Student Survey',font='Verdana 15 bold',bg='#9B90C2',padx=10,pady=10).pack()

# Selections name
FullName = tk.Label(center_frame1,text='Full name : ',anchor='w',font='Verdana 10',padx=30,pady=-120).pack(fill='both')
Residency = tk.Label(center_frame1,text='Residency : ',anchor='w',font='Verdana 10',padx=30,pady=10).pack(fill='both')
Program = tk.Label(center_frame1,text='Program : ',anchor='w',font='Verdana 10',padx=30,pady=20).pack(fill='both')
Courses = tk.Label(center_frame1,text='Courses : ',anchor='w',font='Verdana 10',padx=30,pady=10).pack(fill='both')

# Selections input - Text
FullNameInput = tk.Entry(center_frame2,font='Verdana 10',bg='white')
FullNameInput.defaultValue='XuTung Jin'
FullNameInput.insert(tk.END,FullNameInput.defaultValue)
FullNameInput.place(x=10,y=50,relwidth=0.8)

# Selections input - Radio
ResidencyS = tk.StringVar(None,"Domestic")
DomesticR = tk.Radiobutton(center_frame2,font='Verdana 10',tristatevalue=0,text='Domestic',anchor='w',variable=ResidencyS,value='Domestic').place(x=10,y=75,relwidth=0.8)
InternationalR = tk.Radiobutton(center_frame2,font='Verdana 10',tristatevalue=0,text='International',anchor='w',variable=ResidencyS,value='International').place(x=10,y=95,relwidth=0.8)

# Selections input - Combo Box
n=tk.StringVar()
ProgramC = ttk.Combobox(center_frame2,textvariable=n)
ProgramC['values']=('AI','Gaming','Health','Software')
ProgramC.current(2)
ProgramC.grid(column=1,row=4)
ProgramC.place(x=10,y=130,relwidth=0.8)

# Selections input - Check Box
programVar = tk.IntVar(value=1)
WebVar = tk.IntVar()
softwareVar = tk.IntVar()
ProgrammingC = tk.Checkbutton(center_frame2,text='Programming I',anchor='w',variable=programVar,state=NORMAL, offvalue=0).place(x=10,y=170,relwidth=0.8)
WebC = tk.Checkbutton(center_frame2,text='Web Page Design',anchor='w',variable=WebVar, offvalue=0).place(x=10,y=190,relwidth=0.8)
SoftwareC = tk.Checkbutton(center_frame2,text='Software Engineering',anchor='w',variable=softwareVar, offvalue=0).place(x=10,y=210,relwidth=0.8)

# Buttons
reset = tk.Button(btm_frame1,text='Reset',anchor='s',padx=5,pady=5,command=reset).place(x=10 , y=15 ,relwidth=0.8)
okay = tk.Button(btm_frame2,text='Okay',anchor='s',padx=5,pady=5,command=okay).place(x=10 , y=15 ,relwidth=0.8)
exit = tk.Button(btm_frame3,text='Exit',anchor='s',padx=5,pady=5,command=exit).place(x=10 , y=15 ,relwidth=0.8)

window.mainloop()
