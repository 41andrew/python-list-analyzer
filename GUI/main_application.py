import tkinter as tk
from tkinter import filedialog


class ChooseSourceFilesFrame(tk.Frame):
    """
    Frame with buttons responsible for choosing input files
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.input_file_btn = tk.Button(parent, text="Choose input file", width=30,
                                        command=lambda: self.add_commands_to_buttons('input'))
        self.eng_file_btn = tk.Button(parent, text="Choose engagements file", width=30,
                                      command=lambda: self.add_commands_to_buttons('eng'))
        self.bda_file_btn = tk.Button(parent, text="Choose bda file", width=30,
                                      command=lambda: self.add_commands_to_buttons('bda'))
        self.prop_file_btn = tk.Button(parent, text="Choose proposals file", width=30,
                                       command=lambda: self.add_commands_to_buttons('prop'))

        self.input_file_lbl = tk.Label(parent, pady=10)
        self.eng_file_lbl = tk.Label(parent, pady=10)
        self.bda_file_lbl = tk.Label(parent, pady=10)
        self.prop_file_lbl = tk.Label(parent, pady=10)

        self.set_widgets_position()

    def set_widgets_position(self):
        self.input_file_btn.grid(row=0)
        self.input_file_lbl.grid(row=1)

        self.eng_file_btn.grid(row=2)
        self.eng_file_lbl.grid(row=3)

        self.bda_file_btn.grid(row=4)
        self.bda_file_lbl.grid(row=5)

        self.prop_file_btn.grid(row=6)
        self.prop_file_lbl.grid(row=7)

    def change_label_text(self, label_name, new_text):
        if label_name == "input":
            self.input_file_lbl['text'] = new_text
        elif label_name == "eng":
            self.eng_file_lbl['text'] = new_text
        elif label_name == "bda":
            self.bda_file_lbl['text'] = new_text
        elif label_name == "prop":
            self.prop_file_lbl['text'] = new_text

    @staticmethod
    def read_file_path_from_filesystem():
        file_path = filedialog.askopenfilename()
        return file_path

    def add_commands_to_buttons(self, button_name):
        file_path = self.read_file_path_from_filesystem()
        self.change_label_text(button_name, file_path)


class MainApplication(tk.Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.choose_source_files_frame = ChooseSourceFilesFrame(self)
        self.grid()
        self.set_widgets_position()

    def set_widgets_position(self):
        self.columnconfigure(0, weight=1)
        self.choose_source_files_frame.grid(row=0, column=0)


def center_window_on_the_screen(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_offset = (screen_width / 2) - (width / 2)
    y_offset = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x_offset, y_offset))

if __name__ == "__main__":

    root = tk.Tk()
    app = MainApplication(parent=root)

    app.master.title("Entity Category Assigner")
    app.master.minsize(800, 600)

    w = 800
    h = 600
    center_window_on_the_screen(root, w, h)

    app.mainloop()
