import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        path_input = "test"
        path_eng = ""

        #<create the rest of your GUI here>
        """file_path = filedialog.askopenfilename()
        print (file_path)
        w = Label(parent, text=file_path)
        w.pack()"""


    def create_widgets(self):

        # Hello label
        self.label = tk.Label(self, text="Program do weryfikacji list z CRM", font=("Arial",22))
        self.label.grid(row=0, columnspan=2, ipadx=10, ipady=10)

        # Hello button
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World"
        self.hi_there["command"] = self.say_hi
        self.hi_there.grid(row=1)

        # Przycisk scieżki
        self.inputBtn = tk.Button(self, text="Kliknij, aby wskazać ścieżkę do pliku .csv", command=self.load_input)
        self.inputBtn.grid(row=2)

        # Przycisk scieżki
        self.inputBtn = tk.Button(self, text="Kliknij, aby dodać engagementy", command=self.load_eng)
        self.inputBtn.grid(row=3)

        # Quit button - color change doesn't work on MacOS
        self.quit = tk.Button(self, text="QUIT", fg="black", bg="red", command=root.destroy)
        self.quit.grid(row=4, sticky=tk.N+tk.S+tk.E+tk.W)

        """""# progress bar
        self.progress = ttk.Progressbar(orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.grid()

        # progress bar button
        self.pbButton = tk.Button(text='foo', command=self.bar).grid()"""


    def say_hi(self):
        messagebox.showinfo("Say Hello", "Hello World")

    def load_input(self):
        file_path = filedialog.askopenfilename()
        #print(file_path)
        self.path_input = file_path
        print(self.path_input)
        # Wydrukowana sciezka do pliku
        self.sciezkaDoPliku = tk.Label(self, text="Wybrano plik: " + self.path_input)
        self.sciezkaDoPliku.grid(row=2, column=1)

    def load_eng(self):
        file_path = filedialog.askopenfilename()
        #print(file_path)
        self.path_eng = file_path
        print(self.path_eng)
        # Wydrukowana sciezka do pliku
        self.sciezkaDoPliku = tk.Label(self, text="Wybrano plik: " + self.path_eng)
        self.sciezkaDoPliku.grid(row=3, column=1)

    def bar(self):
        import time
        self.progress['value']=20
        self.update_idletasks()
        time.sleep(1)
        self.progress['value']=50
        self.update_idletasks()
        time.sleep(1)
        self.progress['value']=100

if __name__ == "__main__":

    root = tk.Tk()

    # nie mam pojęcia co to robi
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)

    # create the application
    app = MainApplication(master=root)

    # give it a title
    app.master.title("Super program")

    # give it a minimum size
    app.master.minsize(400, 200)
    w = 600
    h = 400

    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # center the window
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # loop the application
    app.mainloop()


