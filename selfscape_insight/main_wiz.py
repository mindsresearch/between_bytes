""" Wizard-style launcher for the SelfScape Insight program.

WARNING:
    This code is not functional and is only a template for the final product.

Version:
    0.3

Author:
    Noah Duggan Erickson
"""

from tkinter import BOTH, W, E, END, DISABLED, Tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import os
import sys
import logging

from main_cli import main

class SelfScapeInsightLauncher(Tk):
    """ Main window for the SelfScape Insight launcher.

    Note:
        This class is not intended to be accessed outside the program.
    """
    def __init__(self):
        super().__init__()

        self.title("SelfScape Insight Launcher")
        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=True)

        self.basic = BasicConfig()
        notebook.add(self.basic, text="Basic Config")

        self.modules = ModuleSelection()
        notebook.add(self.modules, text="Module Selection")

        self.advanced = AdvConfig()
        notebook.add(self.advanced, text="Advanced Config")

        self.run_button = ttk.Button(self, text="Launch", command=self.run)
        self.run_button.pack()

    def run(self):
        self.run_button.config(state=DISABLED)
        in_dir = self.basic.get_in_directory()
        if in_dir == "":
            logging.critical("No input directory selected")
            raise ValueError("No input directory selected")
        print(f"Input dir:\n  {in_dir}")
        out_dir = self.basic.get_out_directory()
        if out_dir == "":
            logging.warning("No output directory selected")
        print(f"Output dir:\n  {out_dir}")
        print(f"Modules:\n  {self.modules.get_mods()}")
        print(f"Log file:\n  {self.advanced.get_log_file()}")
        print(f"Dev mode:\n  {self.advanced.get_is_dev()}")
        print(f"Do PKL out:\n  {self.advanced.get_out_pkl()}")
        if self.advanced.get_out_pkl():
            out_pkl = os.path.join(out_dir, "data")
        else:
            out_pkl = "temp"
        main(in_dir, self.modules.get_mods(),
             verbose=(2 if self.advanced.get_is_dev() else 0),
             pklroot=out_pkl, log=self.advanced.get_log_file()
             )
        self.destroy()

class BasicConfig(ttk.Frame):
    """ Launcher basic configuration frame.

    Basic config frame to be added to launcher main notebook

    Note:
        This class is not intended to be accessed outside this module.
    """
    def __init__(self):
        super().__init__()

        basic_label = ttk.Label(self, text="Basic Config")
        basic_label.grid(row=0, column=0, columnspan=3)

        in_directory_label = ttk.Label(self, text="Input Directory:")
        in_directory_label.grid(row=1, column=0, sticky=W)

        self.in_directory_entry = ttk.Entry(self, width=50)
        self.in_directory_entry.grid(row=1, column=1, sticky=(W, E))

        in_directory_button = ttk.Button(self, text="Browse",
                                         command=self.select_in_directory)
        in_directory_button.grid(row=1, column=2)

        out_directory_label = ttk.Label(self, text="Output Directory:")
        out_directory_label.grid(row=2, column=0, sticky=W)

        self.out_directory_entry = ttk.Entry(self, width=50)
        self.out_directory_entry.grid(row=2, column=1, sticky=(W, E))

        out_directory_button = ttk.Button(self, text="Browse",
                                          command=self.select_out_directory)
        out_directory_button.grid(row=2, column=2)

    def select_in_directory(self):
        folder_selected = filedialog.askdirectory()
        self.in_directory_entry.delete(0, END)
        self.in_directory_entry.insert(0, folder_selected)

    def select_out_directory(self):
        temp = self.get_out_directory()
        folder_selected = filedialog.askdirectory()
        if len(os.listdir(folder_selected)) > 0:
            resp = messagebox.askyesnocancel(title="Warning",
                                             message="Output directory is not empty. Files may be overwritten.\nCreate new subdirectory?", # pylint: disable=line-too-long
                                             icon="warning")
            if resp is None:
                folder_selected = temp
            elif resp:
                print("Creating /output directory")
                # os.makedirs(folder_selected + "/output")
                folder_selected += "/ssi_output"

        self.out_directory_entry.delete(0, END)
        self.out_directory_entry.insert(0, folder_selected)

    def get_in_directory(self):
        return self.in_directory_entry.get()

    def get_out_directory(self):
        return self.out_directory_entry.get()

class ModuleSelection(ttk.Frame):
    """ Launcher feature module selection frame.

    Feature module selection frame to be added to launcher main notebook

    Note:
        This class is not intended to be accessed outside this module.
    """
    def __init__(self):
        super().__init__()

        mod_label = ttk.Label(self, text="Module Selection")
        mod_label.grid(row=0, column=0, columnspan=5)

        self.mod_1 = ttk.Checkbutton(self, text="Sample")
        self.mod_1.grid(row=1, column=0, sticky=(W, E))
        self.mod_1.invoke()
        self.mod_2 = ttk.Checkbutton(self, text="IP Location")
        self.mod_2.grid(row=1, column=1, sticky=(W, E))
        self.mod_2.invoke()
        self.mod_3 = ttk.Checkbutton(self, text="Off-Facebook Activity")
        self.mod_3.grid(row=1, column=2, sticky=(W, E))
        self.mod_3.invoke()
        self.mod_4 = ttk.Checkbutton(self, text="Topics")
        self.mod_4.grid(row=1, column=3, sticky=(W, E))
        self.mod_4.invoke()
        self.mod_5 = ttk.Checkbutton(self, text="Feelings")
        self.mod_5.grid(row=1, column=4, sticky=(W, E))
        self.mod_5.invoke()

    def get_mods(self):
        return {
            "smp": self.mod_1.instate(["selected"]),
            "ipl": self.mod_2.instate(["selected"]),
            "ofa": self.mod_3.instate(["selected"]),
            "tps": self.mod_4.instate(["selected"]),
            "fgs": self.mod_5.instate(["selected"])
        }

class AdvConfig(ttk.Frame):
    """ Launcher advanced configuration frame.

    Advanced config frame to be added to launcher main notebook

    Note:
        This class is not intended to be accessed outside this module.
    """
    def __init__(self):
        super().__init__()

        adv_label = ttk.Label(self, text="Advanced Config")
        adv_label.grid(row=0, column=0, columnspan=3)

        log_file_label = ttk.Label(self, text="Log File:")
        log_file_label.grid(row=1, column=0, sticky=W)

        self.log_file_entry = ttk.Entry(self, width=50)
        self.log_file_entry.grid(row=1, column=1, sticky=(W, E))

        log_file_button = ttk.Button(self, text="Browse",
                                     command=self.select_new_log_filename)
        log_file_button.grid(row=1, column=2)

        self.dev_button = ttk.Checkbutton(self, text="Dev mode")
        self.dev_button.grid(row=2, column=0, sticky=W)

        self.bp_button = ttk.Checkbutton(self, text="Send data to output dir")
        self.bp_button.grid(row=2, column=1, sticky=W)

    def select_new_log_filename(self):
        log_file = filedialog.asksaveasfilename()
        self.log_file_entry.delete(0, END)
        self.log_file_entry.insert(0, log_file)

    def get_log_file(self):
        return self.log_file_entry.get() or sys.stdout
    def get_is_dev(self):
        return self.dev_button.instate(["selected"])
    def get_out_pkl(self):
        return self.bp_button.instate(["selected"])

if __name__ == "__main__":
    launcher = SelfScapeInsightLauncher()
    launcher.mainloop()
