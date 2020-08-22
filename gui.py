from tkinter import *
from tkinter import filedialog
root = Tk()

# Browse for a file
def browsefunc():
    filename = filedialog.askopenfilename(filetypes=[("Mailbox archive", ".mbox"), ("CSV", ".csv")])
    pathlabel.config(text=filename)

browsebutton = Button(root, text="Browse", command=browsefunc)
browsebutton.pack()

pathlabel = Label(root)
pathlabel.pack()