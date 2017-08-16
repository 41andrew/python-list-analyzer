import tkinter as tk
from tkinter import filedialog
from tkinter import *

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #<create the rest of your GUI here>
        file_path = filedialog.askopenfilename()
        print (file_path)
        w = Label(parent, text=file_path)
        w.pack()

if __name__ == "__main__":
    root = tk.Tk()
    #root.withdraw()


    MainApplication(root).pack(side="top", fill="both", expand=True, padx=200, pady=200)
    root.mainloop()


