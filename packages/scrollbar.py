from tkinter import *

def fill_list_scrollbar(items):
    top = Tk()
    top.geometry('1024x400')
    top.title('Relação de e-mails que foram enviados')

    sb = Scrollbar(top)  
    sb.pack(side = RIGHT, fill = Y)  
    
    mylist = Listbox(top, yscrollcommand = sb.set, width='1024', height='400')  
    
    for line in items:  
        mylist.insert(END, line)  
    
    mylist.pack(side = LEFT)  
    sb.config(command = mylist.yview)  
