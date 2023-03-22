from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import re
import os

#GLOBAL VARIABLE DICTIONARY
dictio = {}

#loading of word in dictio, COUNT frequency of word
def addToDictio(word):
    if word in dictio:
        dictio.update({word : dictio.get(word)+1})
    else:
        dictio[word] = 1

#FILE READING
def loadFile(filename):
    fileReader = open(filename, "r")
    line=[]

    for line in fileReader:
        line = line.strip().split(" ")
        #TOKENIZE-CLEAN
        for i in line:
            i = re.sub("[^a-zA-Z0-9]", "", i)
            # line[i] = re.sub("[\t\r\n\f]", "", line[i])
            if len(i) != 0 :
                addToDictio(i.lower())
        # print(line)
    
    fileReader.close()


# def printDictio():
#     count= 0
#     #SORT dictio before printing in terminal
#     for i in sorted (dictio) :
#         print ((i, dictio[i]), end ="\n")
#         #INSERT IN TABLE
#         table_tbl.insert(parent='',index='end',iid=count,text='',tag='ok',
#         values=(i, dictio[i]))
#         count += 1  #table index
    

def browseFiles():
    filename = filedialog.askopenfilename(
        title = "Select a File"
        # filetypes = (("Text files","*.txt*"),("all files", "*.*"))
    )
    #clear dictionary and items in table
    dictio.clear()
    for item in table_tbl.get_children():
        table_tbl.delete(item)

    if filename != ():
        loadFile(filename)
        # printDictio()
        lb_ds.configure(text=str(len(dictio)))  #update dictionary size label
        dictio_size = len(dictio)
        total_words = countTotalWords()
        writeOutput(filename, dictio_size, total_words)


def countTotalWords():
    total = 0

    for i in dictio:
        total = total + dictio[i]

    print(total)
    lb_tw.configure(text=str(total))    #update total words label
    return total

#FILE WRITING
def writeOutput(filename, dictio_size, total_words):
    new_file = os.path.basename(filename)
    new_file = new_file.split(".")
    new_file[0] = new_file[0] + "-output"
    new_filename = new_file[0] + '.txt'
    print(new_filename)

    fileWriter = open(new_filename, "w")
    fileWriter.write("Dictionary Size: " + str(dictio_size) + "\n")
    fileWriter.write("Total Number of Words: " + str(total_words))

    count = 0
    for i in sorted (dictio):
        fileWriter.write("\n" + str(i) + " " + str(dictio[i]))
        # print ((i, dictio[i]), end ="\n")
        #INSERT IN TABLE
        table_tbl.insert(parent='',index='end',iid=count,text='',tag='ok',
        values=(i, dictio[i]))
        count += 1  #table index

    fileWriter.close()

#MAIN

window = Tk()
window.title("Bag-of-Words")
window.geometry("500x500")
window.resizable(False, False)
window.config(background = "#222222")

browse_btn = Button(window,
    text = "Browse File",
    font="Helvetica",
    bg="#df692a",
    fg="white",
    activeforeground="white",
    activebackground="#222222",
    highlightbackground="#df692a",
    relief="flat",
    command = browseFiles)
browse_btn.place(relx = 0.95, rely=0.05, anchor=NE)

#DICTIONARY SIZE
Label(window,
    text='Dictionary Size:',
    font="Helvetica",
    bg="#222222",
    fg="white"
).place(x=120,y=100)
# dictio_size = str(len(dictio))
lb_ds = Label(window, text="", font="Helvetica", bg="#eeeeee", width=15)
lb_ds.place(x=250,y=100)

#TOTAL WORDS
Label(window,
    text='Total Words:',
    font="Helvetica",
    bg="#222222",
    fg="white"
).place(x=120,y=140)
# total_words = str(countTotalWords())
lb_tw = Label(window, text="", font="Helvetica", bg="#eeeeee", width=15)
lb_tw.place(x=250,y=140)

#TABLE OF WORDS
table_frm = Frame(window, width=300, bg="#eeeeee")
table_frm.place(x=95, y=180)

table_tbl = ttk.Treeview(table_frm, selectmode='none', height="12")
# table_tbl.tag_configure("ok", activebackground="#df692a")
table_tbl['columns'] = ('word', 'frequency')

#column name/id
table_tbl.column("#0", width=0, stretch=NO)
table_tbl.column("word",anchor=CENTER, width=150)
table_tbl.column("frequency",anchor=CENTER, width=150)

#TABLE HEADINGS
table_tbl.heading("#0",text="",anchor=CENTER)
table_tbl.heading("word", text="WORD", anchor=CENTER)
table_tbl.heading("frequency", text="FREQUENCY", anchor=CENTER)

scrllbr = Scrollbar(table_frm, orient=VERTICAL, bg="#df692a")
scrllbr.pack(side=RIGHT, fill=Y)
table_tbl.config(yscrollcommand=scrllbr.set)
scrllbr.config(command=table_tbl.yview)

table_tbl.pack()

window.mainloop()