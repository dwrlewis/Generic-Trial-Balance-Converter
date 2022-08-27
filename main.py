import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import tix
from file_selection import FileSelect
from option_selection import PrefixOptions
from duplicate_correction import DuplicateCorrection
from coa_mapping import CoaConfigure
from data_export import DataExport

# region Pandas Display Options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', 15)
pd.set_option('display.width', None)
# endregion


class MainFrame:
    def __init__(self, master):
        # region Master Options
        master.title('Trial Balance Batch Converter')
        master.geometry('900x700')
        master.minsize(900, 700)
        # endregion

        # region Master Variables
        # file_selection variables
        self.raw_tb = pd.DataFrame()
        self.raw_coa = pd.DataFrame()
        self.raw_company = pd.DataFrame()

        # option_selection variables
        self.prefix_on = False
        self.prefixed_tb = pd.DataFrame()
        self.prefix_accepted = False

        # duplicate_corrections variables
        self.desc_on = False
        self.final_tb = pd.DataFrame()
        self.desc_accepted = False

        # coa_Mappings variables
        self.final_coa = pd.DataFrame()
        self.coa_accepted = False
        # endregion

        # region Classes
        master_tab = ttk.Notebook(master)
        master_tab.grid(row=0, column=0, sticky='nsew')
        self.file_select = FileSelect(master_tab, main=self)
        self.options_select = PrefixOptions(master_tab, main=self)
        self.duplicate_correction = DuplicateCorrection(master_tab, main=self)
        self.coa_mapping = CoaConfigure(master_tab, main=self)
        self.export = DataExport(master_tab, main=self)

        self.colour(master)  # Adds Tkinter Theme
        # endregion

    def colour(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            widget_type = child.winfo_class()

            if widget_type == 'Frame':
                child.config(bg='#282828', highlightbackground='#FFFFFF', highlightthickness=1)
            if widget_type == 'Label':
                child.config(bg='#282828', fg='#FFFFFF', font=('Segoe UI', 10))
            if widget_type == 'Button':
                child.config(bg='#404040', fg='#FFFFFF', font=('Segoe UI', 10))
            if widget_type == 'Canvas':
                child.config(bg='#404040')
            if widget_type == 'Checkbutton':
                child.config(bg='#282828', selectcolor='#282828', fg='#FFFFFF', bd=3, activebackground='#282828',
                             activeforeground='#FFFFFF', font=('Segoe UI', 10))
            if widget_type == 'Scrollbar':
                child.config(bg='#404040')
            if widget_type == 'Entry':
                child.config(bg='#D7D7D7', disabledbackground='#282828')
            if widget_type == 'Radiobutton':
                child.config(bg='#282828', fg='#FFFFFF', activebackground='#282828', activeforeground='#FFFFFF',
                             selectcolor='grey', font=('Segoe UI', 10))
            if widget_type == 'TCombobox':
                pass

            else:
                self.colour(child)


if __name__ == '__main__':
    root = tix.Tk()

    # Add Weights to GUI
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    MainFrame(root)
    root.mainloop()
