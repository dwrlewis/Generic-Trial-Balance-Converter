import tkinter as tk
from tkinter import filedialog
from tkinter import tix
import pandas as pd
import os


class FileSelect:
    def __init__(self, master, main):
        self.master = master
        self.main = main
        self.import_selections = []

        # ================== 0.0 - Top Frame ==================
        self.top_frame = tk.Frame(master)
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.master.add(self.top_frame, text='Import Selection')
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)

        # ================== 1.0 - File Selection Frame ==================
        self.fp_frame = tk.Frame(self.top_frame)
        self.fp_frame.grid(row=0, column=0, sticky='NSEW')
        # Button - Select Directory
        self.fp_button = tk.Button(self.fp_frame, text='Open:', command=self.directory_path, height=2)
        self.fp_button.grid(row=0, column=0, sticky='W')
        # Label - Display Directory
        self.fp_text = tk.StringVar(value='Select Import Directory')
        self.fp_label = tk.Label(self.fp_frame, textvariable=self.fp_text, anchor='w')
        self.fp_label.grid(row=0, column=1, sticky='W')

        # ================== 2.0 - Main Canvas Frame ==================
        self.can_frame = tk.Frame(self.top_frame)
        self.can_frame.grid(row=1, column=0, sticky='NSEW')
        self.can_frame.columnconfigure(0, weight=1)
        self.can_frame.rowconfigure(1, weight=1)
        # ================== 2.1 - Header Canvas Frame ==================
        # Header Canvas
        self.head_can = tk.Canvas(self.can_frame, height=22)
        self.head_can.grid(row=0, column=0, columnspan=5, sticky='EW')
        self.head_can.bind('<Configure>', self.frame_width)
        # Header Canvas Sub-Frame
        self.head_can_sub_frame = tk.Frame(self.head_can)
        self.head_can_sub_frame.bind('<Configure>', self.config_frame)
        self.head_can_sub_frame.columnconfigure(0, weight=1)
        # Header canvas Window
        self.head_can_window = self.head_can.create_window(0, 0, anchor='nw', window=self.head_can_sub_frame)
        # Header Canvas Labels
        self.head_label = tk.Label(self.head_can_sub_frame, text='TB File')
        self.head_label.grid(row=0, column=0)
        # Header Canvas Buttons
        self.head_list = []
        for header_name, col in zip(['Prior', 'Opening', 'Closing', 'COA'], range(1, 5)):
            head_button = tk.Button(self.head_can_sub_frame, text=header_name, anchor='center')
            head_button.grid(row=0, column=col, sticky='EW')
            head_button.bind('<1>', self.period_import_toggle)
            head_button['state'] = 'disabled'
            self.head_list.append(head_button)
            self.head_can_sub_frame.columnconfigure(col, weight=1)
        # ================== 2.2 - Data Canvas Frame ==================
        self.data_can = tk.Canvas(self.can_frame, bg='#BDCDFF')
        self.data_can.grid(row=1, column=0, columnspan=5, sticky='NSEW')
        self.data_can.bind('<Configure>', self.frame_width)
        self.data_can.rowconfigure(0, weight=1)
        # Main Canvas Sub-Frame
        self.data_can_sub_frame = tk.Frame(self.data_can)
        for col in range(5):
            self.data_can_sub_frame.columnconfigure(col, weight=1)
        self.data_can_sub_frame.bind('<Configure>', self.config_frame)
        # Main Canvas Window
        self.data_can_window = self.data_can.create_window(0, 0, anchor='nw', window=self.data_can_sub_frame)
        # Scrollbar
        self.data_can_scroll = tk.Scrollbar(self.can_frame, orient="vertical", command=self.data_can.yview)
        self.data_can_scroll.grid(row=1, column=5, sticky='NS')

        # ================== 3.0 - load Files Frame ==================
        self.load_frame = tk.Frame(self.top_frame)
        self.load_frame.grid(row=2, column=0, sticky='NSEW')
        # Load Files Trim Nulls Checkbox
        self.load_on_off = tk.IntVar(value=0)
        self.load_checkbox = tk.Checkbutton(self.load_frame, text='Filter null amounts', variable=self.load_on_off)
        self.load_checkbox.grid(row=0, column=0)
        # Load Files Button
        self.load_button = tk.Button(self.load_frame, text='Load Trial Balances', command=self.load_files, height=3)
        self.load_button.grid(row=1, column=0, sticky='EW')
        # Load Files Label
        self.load_label = tk.Label(self.load_frame, text='', anchor='w')
        self.load_label.grid(row=1, column=1, sticky='NSW')

    # GUI resizing functions
    def frame_width(self, event):
        # Updates widths of main and header canvas when adjusted to fit window
        canvas_width = event.width
        event.widget.itemconfigure(self.data_can_window, width=canvas_width)

    def config_frame(self, _):
        # Called when size of header/data subframe are adjusted to align with canvas size
        self.data_can.configure(scrollregion=self.data_can.bbox('all'), yscrollcommand=self.data_can_scroll.set)
        # Reset headers is then called to align header data
        self.data_can.after_idle(self.reset_headers)

    def reset_headers(self):
        # Matches header canvas to main canvas when expanded
        for column in range(self.data_can_sub_frame.grid_size()[0]):
            bbox = self.data_can_sub_frame.grid_bbox(column, 0)
            self.head_can_sub_frame.columnconfigure(column, minsize=bbox[2])

    # Directory selections functions
    def directory_path(self):
        try:
            # 1) Select filepath and update tkinter text with path
            fp = filedialog.askdirectory(initialdir='/', title='Select a directory')

            # 2) Sets GUI label to selected filepath, exits function if not selected
            if len(fp) != 0:
                self.fp_text.set(str(fp))
                self.fp_label.config(fg='#8ace7e')
            else:
                self.fp_text.set('ERROR: No Filepath was selected')
                self.fp_label.config(fg='#ff684c')
                for button in self.head_list:
                    button['state'] = 'disable'
                return

            # 3) Find .xlsm files in folder , exits function if none found
            tb_files = [file for file in os.listdir(fp) if file.endswith('.xlsm') and not file.startswith('~$')]
            if len(tb_files) == 0:
                self.fp_text.set('ERROR: Directory contains no .xlsm formatted files')
                self.fp_label.config(fg='#ff684c')
                for button in self.head_list:
                    button['state'] = 'disable'
                return

            # 4) Clears import selections list and changes filepath
            self.import_selections.clear()
            os.chdir(fp)

            # 5) Generates GUI and saves elements to access load selections
            for tb in tb_files:
                y = tb_files.index(tb)
                elements = []

                # Creates file name button
                file_name = tk.Button(self.data_can_sub_frame, text=tb, anchor='w', bg='#a3acb9')
                file_name.grid(row=y, column=0, sticky='EW')
                file_name.bind('<1>', self.file_import_toggle)
                elements.append(file_name)

                # Creates 4 checkboxes for prior, opening, closing and COA
                for x in range(4):
                    check = tk.IntVar(value=1)
                    period = tk.Checkbutton(self.data_can_sub_frame, anchor='center', bg='#C2D0F9', variable=check)
                    period.grid(row=y, column=x + 1, sticky='EW')
                    elements.append([period, check])

                # Add each row of gui elements, creating nested list
                self.import_selections.append(elements)

            for button in self.head_list:
                # Enables header buttons for selecting period imports on/off
                button['state'] = 'normal'

        # Filepath error handling exception
        except os.error:
            self.fp_text.set('ERROR: Invalid Directory')
            self.fp_label.config(fg='#ff684c')
            for button in self.head_list:
                button['state'] = 'disable'

    def file_import_toggle(self, event):
        # Get row number
        row = event.widget.grid_info()['row']

        # Searches for unticked checkboxes
        all_checks_on = True
        for x in self.import_selections[row][1:]:
            if x[1].get() == 0:
                all_checks_on = False
                break

        # map checks on/off based on all_checks_on variable
        for x in self.import_selections[row][1:]:
            x[1].set(0) if all_checks_on else x[1].set(1)

    def period_import_toggle(self, event):
        # Get column number
        col = event.widget.grid_info()['column']

        # Searches for unticked checkboxes
        all_checks_on = True
        for x in self.import_selections:
            if x[col][1].get() == 0:
                all_checks_on = False
                break

        # maps checks on/off based on all_checks_on variable
        for x in self.import_selections:
            x[col][1].set(0) if all_checks_on else x[col][1].set(1)

    # File import function
    def load_files(self):
        # 1) Reset internal dataframes, remove any balloon popups to prevent erroneous looping in winfo_children()
        self.main.raw_tb = pd.DataFrame()
        self.main.raw_coa = pd.DataFrame()
        self.main.raw_company = pd.DataFrame()

        raw_tb = pd.DataFrame()
        raw_coa = pd.DataFrame()
        no_viable_tabs = True  # Error Handling in case there is no valid data

        self.main.prefix_on = False
        self.main.prefix_accepted = False
        # duplicate_corrections
        self.main.desc_on = False
        self.main.desc_accepted = False
        # coa_Mappings
        self.main.coa_accepted = False

        for child in self.data_can_sub_frame.winfo_children():
            widget_type = child.winfo_class()
            if widget_type == 'TixBalloon':
                child.destroy()

        # 2) Get widgets in canvas after excluding tixballoons, convert into 5 column nested list to loop by row
        widgets = self.data_can_sub_frame.winfo_children()
        import_selections = [widgets[y:y + 5] for y in range(0, len(widgets), 5)]

        # 3) Loop through each row, importing TB data per selected checkboxes
        for row in import_selections:
            # 4) Map each tkinter element to a variable for ease of script readability
            file_name = row[0]['text']
            period_selections = {row[1]: 'Prior TB', row[2]: 'Opening TB', row[3]: 'Closing TB'}
            row[4]: tk.Checkbutton
            coa = row[4]

            # 5) Attempt to load TB file
            try:
                data = pd.ExcelFile(file_name)
                # 6) Load each TB period dependent on selections
                period: tk.Checkbutton()  # Must explicitly declare type to prevent attribute errors
                headers = [['Prior Company', 'Prior Account Code', 'Prior Account Name', 'Prior Amount'],
                           ['Opening Company', 'Opening Account Code', 'Opening Account Name', 'Opening Amount'],
                           ['Closing Company', 'Closing Account Code', 'Closing Account Name', 'Closing Amount']]
                for period, header in zip(period_selections, headers):
                    selection = str(period.cget("variable"))
                    if int(period.getvar(selection)) == 1:
                        try:
                            # 6.0) Check if headers data matches format of advantage template (ADJUST, LOADS TWICE)
                            col_list = [header for header in pd.read_excel(data, sheet_name=period_selections[period],
                                                                           usecols='A:D').columns]
                            if col_list != header:
                                period.config(bg='#ff684c')
                                error_message = 'Tab has non-standard headers for advantage template.'
                                error_popup = tix.Balloon(self.data_can_sub_frame)
                                error_popup.config(bg='#ffda66')
                                error_popup.bind_widget(period, balloonmsg=error_message)
                                continue

                            # 6.1) Load Tab
                            tab = pd.read_excel(data, sheet_name=period_selections[period], usecols='A:D',
                                                names=['Company', 'Code', 'Desc.', 'Amount'],
                                                converters={'Company': str, 'Code': str, 'Desc.': str, 'Amount': float})
                            # tab['Amount'].round(2)  Rounds to 2dp, useless since removed on export, adds load time
                            tab.insert(0, 'TB Period', period_selections[period])
                            tab.insert(0, 'Filename', file_name)

                            # 6.2) Filter out zero values if checkbox selected
                            if self.load_on_off.get() == 1:
                                tab = tab[tab['Amount'] != 0]
                                tab.dropna(subset=['Amount'], inplace=True)

                            # 6.3) Check for errors in period tab
                            minor_flag = False
                            major_flag = False
                            error_notes = []

                            # Blank field check
                            for column in tab.columns.values[2:7]:
                                if tab[column].isnull().any():
                                    major_flag = True if column in ['Company', 'Code'] else major_flag
                                    minor_flag = True if column in ['Desc.', 'Amount'] else minor_flag
                                    error_notes.append('* Null ' + str(column) + ' entries found.')

                            # Overall imbalance check
                            if tab['Amount'].sum() > 2 or tab['Amount'].sum() < -2:
                                minor_flag = True
                                error_notes.append('* Amount field has imbalance of ' + str(tab['Amount'].sum()))

                            # Add Balloon Note for errors when hove#ff684c over
                            error_notes_list = '\n'.join(error_notes)
                            error_popup = tix.Balloon(self.data_can_sub_frame)
                            error_popup.config(bg='#ffda66')
                            error_popup.bind_widget(period, balloonmsg=error_notes_list)
                            # Update label colours
                            if major_flag:
                                period.config(bg='#ff684c')
                            elif minor_flag:
                                period.config(bg='#ffda66')
                            else:
                                period.config(bg='#8ace7e')

                            # 6.4) Add data to main dataframe
                            if not major_flag:
                                raw_tb = pd.concat([raw_tb, tab])
                                no_viable_tabs = False

                        except Exception as error:
                            # Turns entire file row #ff684c and flags with error
                            period.config(bg='#ff684c')
                            error_message = str(error)
                            error_popup = tix.Balloon(self.data_can_sub_frame)
                            error_popup.config(bg='#ffda66')
                            error_popup.bind_widget(period, balloonmsg=error_message)
                    else:
                        # Sets tab checkbutton to default colour if not imported
                        period.config(bg='#C2D0F9')

                # 7) Load COA data dependent on selections
                selection = str(coa.cget("variable"))
                coa: tk.Checkbutton()  # Must explicitly declare type to prevent attribute errors
                if int(coa.getvar(selection)) == 1:
                    try:
                        col_list = [header for header in pd.read_excel(data, sheet_name='Chart of Accounts',
                                                                       usecols='A:C').columns]
                        if col_list != ['CoA Account Code', 'CoA Account Name', 'BDO FSA']:
                            coa.config(bg='#ff684c')
                            error_message = 'Tab has non-standard headers for advantage template.'
                            error_popup = tix.Balloon(self.data_can_sub_frame)
                            error_popup.config(bg='#ffda66')
                            error_popup.bind_widget(coa, balloonmsg=error_message)
                            continue

                        # 7.1) Load COA data
                        coa_data = pd.read_excel(data, sheet_name='Chart of Accounts', usecols='A:C',
                                                 names=['Code', 'Desc.', 'FSA'],
                                                 converters={'Code': str, 'Desc.': str, 'FSA': str})

                        # 7.2) Drop any lines with no account, desc. or mapping, then drop null FSA's
                        coa_data.dropna(how='all', inplace=True)
                        coa_data.dropna(subset=['FSA'], inplace=True)
                        # 7.3) Add Filename field
                        coa_data.insert(0, 'Filename', file_name)

                        # 7.4) Check for errors in COA data
                        coa_minor_flag = False
                        coa_major_flag = False
                        coa_error_notes = []

                        # Blank field check
                        for column in coa_data.columns.values[1:4]:
                            if coa_data[column].isnull().any():
                                coa_major_flag = True if column == ['Code'] else False
                                coa_minor_flag = True if column != ['Code'] else False
                                coa_error_notes.append('* Null ' + str(column) + ' entries found.')

                        # Add Balloon Note for errors
                        coa_error_notes_list = '\n'.join(coa_error_notes)
                        error_popup = tix.Balloon(self.data_can_sub_frame)
                        error_popup.config(bg='#ffda66')
                        error_popup.bind_widget(coa, balloonmsg=coa_error_notes_list)
                        # Update label colours
                        if coa_major_flag:
                            coa.config(bg='#ff684c')
                        elif coa_minor_flag:
                            coa.config(bg='#ffda66')
                        else:
                            coa.config(bg='#8ace7e')

                        # 7.5) Add data to main dataframe
                        if not coa_major_flag:
                            raw_coa = pd.concat([raw_coa, coa_data])
                            no_viable_tabs = False

                    except Exception as error:
                        # Must explicitly declare type to prevent attribute errors
                        coa: tk.Checkbutton()
                        # Turns entire file row #ff684c and flags with error
                        coa.config(bg='#ff684c')
                        error_message = str(error)
                        error_popup = tix.Balloon(self.data_can_sub_frame)
                        error_popup.config(bg='#ffda66')
                        error_popup.bind_widget(coa, balloonmsg=error_message)
                else:
                    # Sets tab checkbutton to default colour if not imported
                    coa.config(bg='#C2D0F9')

            except Exception as error:
                for period in period_selections:
                    period: tk.Checkbutton  # Must explicitly declare type to prevent attribute errors
                    # Turns entire file row #ff684c and flags with error
                    period.config(bg='#ff684c')
                    error_message = str(error)
                    error_popup = tix.Balloon(self.data_can_sub_frame)
                    error_popup.config(bg='#ffda66')
                    error_popup.bind_widget(period, balloonmsg=error_message)

        # 9) Check if any data was imported from PY, OP, or CL tabs
        if not no_viable_tabs and not raw_tb.empty:
            # 10) Update GUI & mainframe data depending on data format
            file_no = pd.concat([raw_tb['Filename'], raw_coa['Filename']])
            raw_company = list(dict.fromkeys(raw_tb['Company']))
            self.load_label.config(text='TB data has been imported for ' + str(file_no.nunique())
                                        + ' files, totalling ' + str(len(raw_tb)) + ' TB lines, and '
                                        + str(len(raw_coa)) + ' COA lines. Please review any errors flagged.',
                                   fg='#8ace7e')

            self.main.raw_tb = raw_tb
            self.main.raw_coa = raw_coa
            self.main.raw_company = raw_company

            for tab in range(1, 3):
                print(tab)
                self.master.tab(tab, state="normal")
        else:
            self.load_label.config(text='ERROR: No viable data found in PY, OP, or CL tabs of any files, '
                                        'or no TB periods were selected for import.',
                                   fg='#ff684c')
            for tab in range(1, 4):
                print(tab)
                self.master.tab(tab, state="disabled")

        print('\n======== RAW TB DATA ========')
        print(self.main.raw_tb)
        print('\n======== RAW COA DATA ========')
        print(self.main.raw_coa)
        # print('\n======== UNIQUE COMPANIES LIST ========')
        # print(self.main.raw_company)
