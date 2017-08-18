import tkinter as tk
from tkinter import filedialog
from data_loader.data_loader import CsvDataLoader


class ChooseSourceFilesFrame(tk.Frame):
    """
    Frame with buttons responsible for choosing input files
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.input_file_btn = tk.Button(parent, text="Choose input file", width=30,
                                        command=lambda: self.change_input_file('input'))
        self.eng_file_btn = tk.Button(parent, text="Choose engagements file", width=30,
                                      command=lambda: self.change_input_file('eng'))
        self.bda_file_btn = tk.Button(parent, text="Choose bda file", width=30,
                                      command=lambda: self.change_input_file('bda'))
        self.prop_file_btn = tk.Button(parent, text="Choose proposals file", width=30,
                                       command=lambda: self.change_input_file('prop'))
        self.crm_file_btn = tk.Button(parent, text="Choose file with CRM entity names", width=30,
                                      command=lambda: self.change_input_file('crm'))

        self.input_file_lbl = tk.Label(parent, pady=10)
        self.eng_file_lbl = tk.Label(parent, pady=10)
        self.bda_file_lbl = tk.Label(parent, pady=10)
        self.prop_file_lbl = tk.Label(parent, pady=10)
        self.crm_file_lbl = tk.Label(parent, pady=10)

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

        self.crm_file_btn.grid(row=8)
        self.crm_file_lbl.grid(row=9)

    def change_label_text(self, label_name, new_text):
        if label_name == "input":
            self.input_file_lbl['text'] = new_text
        elif label_name == "eng":
            self.eng_file_lbl['text'] = new_text
        elif label_name == "bda":
            self.bda_file_lbl['text'] = new_text
        elif label_name == "prop":
            self.prop_file_lbl['text'] = new_text
        elif label_name == "crm":
            self.crm_file_lbl['text'] = new_text
            pass

    def pass_new_path_to_parent(self, path_name, path_value):
        self.parent.change_path_in_data_loader(path_name, path_value)

    @staticmethod
    def read_file_path_from_filesystem():
        file_path = filedialog.askopenfilename()
        return file_path

    def change_input_file(self, button_name):
        file_path = self.read_file_path_from_filesystem()
        self.change_label_text(button_name, file_path)
        self.pass_new_path_to_parent(button_name, file_path)


class MainApplication(tk.Frame):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Window elements
        self.choose_source_files_frame = ChooseSourceFilesFrame(self)

        # Other attributes needed for calculations
        self.data_loader = CsvDataLoader()

        self.grid()
        self.set_widgets_position()

    def set_widgets_position(self):
        self.columnconfigure(0, weight=1)
        self.choose_source_files_frame.grid(row=0, column=0)

    def change_path_in_data_loader(self, path_key, path_value):
        if path_key == "input":
            self.data_loader.data_paths['input_file_source'] = path_value
        elif path_key == "eng":
            self.data_loader.data_paths['input_file_engagements'] = path_value
        elif path_key == "bda":
            self.data_loader.data_paths['input_file_bda'] = path_value
        elif path_key == "prop":
            self.data_loader.data_paths['input_file_proposals'] = path_value
        elif path_key == "crm":
            # TODO - not yet implemented
            pass


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
