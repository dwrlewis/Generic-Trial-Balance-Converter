import tkinter as tk
from tkinter import filedialog
from tkinter import tix
import pandas as pd
import os


class FileSelect:
    def __init__(self, master, main):
        self.master = master
        self.main = main

        # region Variables
        self.import_selections = []  # List containing GUI checkbutton widgets to retain selections
        # endregion

        # region ================== 0.0 - Top Frame ==================
        self.top_frame = tk.Frame(master)
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)

        self.master.add(self.top_frame, text='Import Selection')
        # endregion

        # region ================== 1.0 - File Selection Frame ==================
        self.fp_frame = tk.Frame(self.top_frame)
        self.fp_frame.grid(row=0, column=0, sticky='NSEW')
        # Select Directory Button
        self.fp_button = tk.Button(self.fp_frame, text='Open:', command=self.directory_path, height=2)
        self.fp_button.grid(row=0, column=0, sticky='W')
        # Directory Display Label
        self.fp_label = tk.Label(self.fp_frame, text='Select Import Directory', anchor='w')
        self.fp_label.grid(row=0, column=1, sticky='W')
        # endregion

        # region ================== 2.0 - Main Canvas Frame ==================
        self.can_frame = tk.Frame(self.top_frame)
        self.can_frame.grid(row=1, column=0, sticky='NSEW')
        self.can_frame.columnconfigure(0, weight=1)
        self.can_frame.rowconfigure(1, weight=1)

        # region ================== 2.1 - Header Canvas Frame ==================
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
        # Header Canvas Label
        self.head_label = tk.Label(self.head_can_sub_frame, text='TB File')
        self.head_label.grid(row=0, column=0)
        # Header Canvas Buttons
        self.head_list = []  # List to access buttons for enabling/disabling checkbutton selections
        for header_name, col in zip(['Prior', 'Opening', 'Closing', 'COA'], range(1, 5)):
            head_button = tk.Button(self.head_can_sub_frame, text=header_name, anchor='center')
            head_button.grid(row=0, column=col, sticky='EW')
            head_button.bind('<1>', self.period_import_toggle)
            head_button['state'] = 'disabled'
            self.head_list.append(head_button)
            self.head_can_sub_frame.columnconfigure(col, weight=1)
        # endregion

        # region ================== 2.2 - Data Canvas Frame ==================
        # Main Canvas
        self.data_can = tk.Canvas(self.can_frame, bg='#BDCDFF')
        self.data_can.grid(row=1, column=0, columnspan=5, sticky='NSEW')
        self.data_can.bind('<Configure>', self.frame_width)
        self.data_can.rowconfigure(0, weight=1)
        # Main Canvas Sub-Frame
        self.data_can_sub_frame = tk.Frame(self.data_can)
        for col in range(5):  # Add column weights to all canvas columns
            self.data_can_sub_frame.columnconfigure(col, weight=1)
        self.data_can_sub_frame.bind('<Configure>', self.config_frame)
        # Main Canvas Window
        self.data_can_window = self.data_can.create_window(0, 0, anchor='nw', window=self.data_can_sub_frame)
        # Scrollbar
        self.data_can_scroll = tk.Scrollbar(self.can_frame, orient='vertical', command=self.data_can.yview)
        self.data_can_scroll.grid(row=1, column=5, sticky='NS')
        # endregion

        # endregion

        # region ================== 3.0 - load Files Frame ==================
        self.load_frame = tk.Frame(self.top_frame)
        self.load_frame.grid(row=2, column=0, sticky='NSEW')
        # Load Files Remove Null Amount Lines Checkbox
        self.load_on_off = tk.IntVar(value=0)
        self.load_checkbox = tk.Checkbutton(self.load_frame, text='Filter null amounts', variable=self.load_on_off)
        self.load_checkbox.grid(row=0, column=0)
        # Load Files Button
        self.load_button = tk.Button(self.load_frame, text='Load Trial Balances', command=self.load_files, height=3)
        self.load_button.grid(row=1, column=0, sticky='EW')
        # Load Files Label
        self.load_label = tk.Label(self.load_frame, text='', anchor='w')
        self.load_label.grid(row=1, column=1, sticky='NSW')
        # endregion

    # region GUI resizing functions
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
    # endregion

    # region Directory selections functions
    def directory_path(self):
        try:
            # region 1) Select filepath and update tkinter text with path
            fp = filedialog.askdirectory(initialdir='/', title='Select a directory')
            # endregion

            # region 2) Sets GUI label to selected filepath, exits function if not selected
            if len(fp) != 0:
                self.fp_label.config(text=str(fp), fg='#8ace7e')
            else:
                self.fp_label.config(text='ERROR: No Filepath was selected', fg='#ff684c')
                for button in self.head_list:
                    button['state'] = 'disable'
                return
            # endregion

            # region 3) Find .xlsm files in folder , exits function if none found
            tb_files = [file for file in os.listdir(fp) if file.endswith('.xlsm') and not file.startswith('~$')]
            if len(tb_files) == 0:
                # self.fp_text.set('ERROR: Directory contains no .xlsm formatted files')
                # self.fp_label.config(fg='#ff684c')
                self.fp_label.config(text='ERROR: Directory contains no .xlsm formatted files', fg='#ff684c')
                for button in self.head_list:
                    button['state'] = 'disable'
                return
            # endregion

            # region 4) Clears import selections list and changes filepath
            self.import_selections.clear()
            os.chdir(fp)
            # endregion

            # region 5) Generates GUI and saves elements to access load selections
            for tb in tb_files:
                y = tb_files.index(tb)  # List positions are used as Y axis GUI grid position
                elements = []  # GUI elements added to list for access when selections are made

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
            # endregion

            # region 6) GUI header buttons are enabled
            for button in self.head_list:
                # Enables header buttons for selecting period imports on/off
                button['state'] = 'normal'
            # endregion

        except Exception as error:
            # region Filepath error handling exception
            self.fp_label.config(text='ERROR: ' + str(error), fg='#ff684c')
            for button in self.head_list:
                button['state'] = 'disable'
            # endregion

    def file_import_toggle(self, event):
        # 1) Get Y axis position of widget selected, search for unselected check buttons on Y axis
        row = event.widget.grid_info()['row']
        all_checks_on = True
        for x in self.import_selections[row][1:]:
            if x[1].get() == 0:
                all_checks_on = False
                break

        # 2) map checks on/off based on all_checks_on variable
        for x in self.import_selections[row][1:]:
            x[1].set(0) if all_checks_on else x[1].set(1)

    def period_import_toggle(self, event):
        # 1) Get X axis position of widget selected, search for unselected check buttons on X axis
        col = event.widget.grid_info()['column']
        all_checks_on = True
        for x in self.import_selections:
            if x[col][1].get() == 0:
                all_checks_on = False
                break

        # 2) map checks on/off based on all_checks_on variable
        for x in self.import_selections:
            x[col][1].set(0) if all_checks_on else x[col][1].set(1)
    # endregion

    # region File import function
    def load_files(self):
        # region 1) Reset all dataframes and variables
        self.main.raw_tb = pd.DataFrame()
        self.main.raw_coa = pd.DataFrame()
        self.main.raw_company = pd.DataFrame()
        raw_tb = pd.DataFrame()
        raw_coa = pd.DataFrame()
        no_viable_tabs = True

        # option_selection
        self.main.prefix_on = False
        self.main.prefix_accepted = False

        # duplicate_correction
        self.main.desc_on = False
        self.main.desc_accepted = False

        # coa_mapping
        self.main.coa_accepted = False

        # Remove any balloon popups to prevent erroneous looping later in the function
        for child in self.data_can_sub_frame.winfo_children():
            widget_type = child.winfo_class()
            if widget_type == 'TixBalloon':
                child.destroy()
        # endregion

        # region 2) Get widgets in canvas after removing tix-balloons, convert into 5 column nested list to loop by row
        widgets = self.data_can_sub_frame.winfo_children()
        import_selections = [widgets[y:y + 5] for y in range(0, len(widgets), 5)]
        # endregion

        # region 3) Loop through each row, importing TB data per selected checkboxes
        for row in import_selections:
            # region 4) Map each tkinter element to a variable for ease of script readability
            file_name = row[0]['text']
            period_selections = {row[1]: 'Prior TB', row[2]: 'Opening TB', row[3]: 'Closing TB'}
            coa = row[4]
            # endregion

            try:
                # region 5) Import file, generate header list to check for in each tab
                data = pd.ExcelFile(file_name)
                headers = [['Prior Company', 'Prior Account Code', 'Prior Account Name', 'Prior Amount'],
                           ['Opening Company', 'Opening Account Code', 'Opening Account Name', 'Opening Amount'],
                           ['Closing Company', 'Closing Account Code', 'Closing Account Name', 'Closing Amount']]
                # endregion

                # region 6) Load each TB period dependent on selections
                period: tk.Checkbutton  # Must explicitly declare type to prevent attribute errors
                for period, header in zip(period_selections, headers):
                    selection = str(period.cget('variable'))  # Used to direct access checkbutton var selection
                    if int(period.getvar(selection)) == 1:
                        try:
                            # region 6.1) Check if header data matches TB template format, else add warning tix balloon
                            col_list = [header for header in pd.read_excel(data, sheet_name=period_selections[period],
                                                                           usecols='A:D').columns]
                            if col_list != header:
                                period.config(bg='#ff684c')
                                error_message = 'Tab has non-standard headers for advantage template.'
                                error_popup = tix.Balloon(self.data_can_sub_frame, bg='#ffda66')
                                error_popup.bind_widget(period, balloonmsg=error_message)
                                continue
                            # endregion

                            # region 6.2) Load Tab (NOTE: Adjust, loads to check headers twice)
                            tab = pd.read_excel(data, sheet_name=period_selections[period], usecols='A:D',
                                                names=['Company', 'Code', 'Desc.', 'Amount'],
                                                converters={'Company': str, 'Code': str, 'Desc.': str, 'Amount': float})
                            tab.insert(0, 'TB Period', period_selections[period])
                            tab.insert(0, 'Filename', file_name)
                            # endregion

                            # region 6.3) Filter out zero values if checkbox selection was made
                            if self.load_on_off.get() == 1:
                                tab = tab[tab['Amount'] != 0]
                                tab.dropna(subset=['Amount'], inplace=True)
                            # endregion

                            # region 6.4) Check for errors in period tab
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
                            # endregion

                            # region 6.5) Add Balloon Note with any errors found to GUI, update colour scheme
                            error_notes_list = '\n'.join(error_notes)
                            error_popup = tix.Balloon(self.data_can_sub_frame, bg='#ffda66')
                            error_popup.bind_widget(period, balloonmsg=error_notes_list)
                            if major_flag:
                                period.config(bg='#ff684c')
                            elif minor_flag:
                                period.config(bg='#ffda66')
                            else:
                                period.config(bg='#8ace7e')
                            # endregion

                            # region 6.6) Add data to main dataframe
                            if not major_flag:
                                raw_tb = pd.concat([raw_tb, tab])
                                no_viable_tabs = False
                            # endregion

                        except Exception as error:
                            # Turns entire file row red and flags with exception error
                            period.config(bg='#ff684c')
                            error_message = str(error)
                            error_popup = tix.Balloon(self.data_can_sub_frame, bg='#ffda66')
                            error_popup.bind_widget(period, balloonmsg=error_message)
                    else:
                        # Sets tab checkbutton to default colour if not imported
                        period.config(bg='#C2D0F9')
                # endregion

                # region 7) Load COA data dependent on selections
                coa: tk.Checkbutton()  # Must explicitly declare type to prevent attribute errors
                selection = str(coa.cget('variable'))  # Used to direct access checkbutton var selection
                if int(coa.getvar(selection)) == 1:
                    try:
                        # region 7.1) Check if header data matches TB template format, else add warning tix balloon
                        col_list = [header for header in pd.read_excel(data, sheet_name='Chart of Accounts',
                                                                       usecols='A:C').columns]
                        if col_list != ['CoA Account Code', 'CoA Account Name', 'BDO FSA']:
                            coa.config(bg='#ff684c')
                            error_message = 'Tab has non-standard headers for advantage template.'
                            error_popup = tix.Balloon(self.data_can_sub_frame, bg='#ffda66')
                            error_popup.bind_widget(coa, balloonmsg=error_message)
                            continue
                        # endregion

                        # region 7.2) Load COA data, drop lines with no account, desc. or mapping, then drop null FSA's
                        coa_data = pd.read_excel(data, sheet_name='Chart of Accounts', usecols='A:C',
                                                 names=['Code', 'Desc.', 'FSA'],
                                                 converters={'Code': str, 'Desc.': str, 'FSA': str})
                        coa_data.dropna(how='all', inplace=True)
                        coa_data.dropna(subset=['FSA'], inplace=True)
                        coa_data.insert(0, 'Filename', file_name)
                        # endregion

                        # region 7.3) Check for errors in COA tab
                        coa_minor_flag = False
                        coa_major_flag = False
                        coa_error_notes = []
                        # Blank field check
                        for column in coa_data.columns.values[1:4]:
                            if coa_data[column].isnull().any():
                                coa_major_flag = True if column == ['Code'] else False
                                coa_minor_flag = True if column != ['Code'] else False
                                coa_error_notes.append('* Null ' + str(column) + ' entries found.')
                        # endregion

                        # region 7.4) Add Balloon Note with any errors found to GUI, update colour scheme
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
                        # endregion

                        # region 7.5) Add data to main COA dataframe
                        if not coa_major_flag:
                            raw_coa = pd.concat([raw_coa, coa_data])
                            no_viable_tabs = False
                        # endregion

                    except Exception as error:
                        # Turns entire file row red and flags with error
                        coa.config(bg='#ff684c')
                        error_message = str(error)
                        error_popup = tix.Balloon(self.data_can_sub_frame)
                        error_popup.config(bg='#ffda66')
                        error_popup.bind_widget(coa, balloonmsg=error_message)
                else:
                    # Sets tab checkbutton to default colour if not imported
                    coa.config(bg='#C2D0F9')
                # endregion

            except Exception as error:
                for period in period_selections:
                    # region Turns entire file row red and flags with error
                    period.config(bg='#ff684c')
                    error_message = str(error)
                    error_popup = tix.Balloon(self.data_can_sub_frame, bg='#ffda66')
                    error_popup.bind_widget(period, balloonmsg=error_message)
                    # endregion
        # endregion

        # region 8) Check if any data was imported from PY, OP, CL or COA tabs, adds to main dataframes
        if not no_viable_tabs and not raw_tb.empty:
            # region 8.1) Assign local variables to root variables to be used in other tabs
            self.main.raw_tb = raw_tb
            self.main.raw_coa = raw_coa
            self.main.raw_company = list(dict.fromkeys(raw_tb['Company']))  # Unique companies variable
            # endregion

            # region 8.2) Update import label with number of files & no. of TB & COA lines
            file_no = pd.concat([raw_tb['Filename'], raw_coa['Filename']])  # Unique Files variables
            self.load_label.config(text='TB data has been imported for ' + str(file_no.nunique()) + ' files, totalling '
                                        + str(len(raw_tb)) + ' TB lines, and ' + str(len(raw_coa)) +
                                        ' COA lines. Please review any errors flagged.', fg='#8ace7e')
            # endregion

            # region 8.3) Enables the Prefix & duplicate description GUI tabs
            for tab in range(1, 3):
                self.master.tab(tab, state='normal')
            # endregion
        else:
            self.load_label.config(text='ERROR: No viable data found in PY, OP, or CL tabs of any files, '
                                        'or no TB periods were selected for import.', fg='#ff684c')
            for tab in range(1, 4):
                self.master.tab(tab, state='disabled')

        # endregion

        # region 9) Prints imported datasets
        # print('\n======== RAW TB DATA ========')
        # print(self.main.raw_tb)
        # print('\n======== RAW COA DATA ========')
        # print(self.main.raw_coa)
        # print('\n======== UNIQUE COMPANIES LIST ========')
        # print(self.main.raw_company)
        # endregion
    # endregion
