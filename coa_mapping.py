import tkinter as tk
from tkinter import ttk
import pandas as pd


class CoaConfigure:
    def __init__(self, master, main):
        self.master = master
        self.main = main
        self.coa = pd.DataFrame()
        self.fsa_limit = False

        self.fsa_list = ['A1-Intangibles',
                         'A1A-Intangibles - Mining',
                         'A1B-Intangibles - Oil and gas',
                         'A2-Property, Plant and Equipment',
                         'A2A-PPE - Mining',
                         'A2B-PPE - Oil and gas',
                         'A2C-Investment properties',
                         'A3-Heritage Assets',
                         'B-Investments',
                         'B2-Investments held at fair value',
                         'B3-Other financial investments',
                         'C-Inventories',
                         'C1-Inventories - raw materials',
                         'C2-Inventories - work in progress',
                         'C3-Inventories - finished goods',
                         'C4-Long Term Work in Progress',
                         'D-Accounts Receivable',
                         'D1-Long Term Receivables',
                         'D2-Loans and advances to customers',
                         'D3-Loans and advances to banks',
                         'D4-Trade Finance',
                         'D5-Cash balances at central banks',
                         'E-Other Receivables or Prepayments',
                         'E1-Short Term Investments',
                         'E2-Deferred Charges',
                         'F-Cash Balances',
                         'F1-Borrowings',
                         'F2-Customer accounts',
                         'F3-Deposits from banks',
                         'G-Accounts Payable',
                         'G1-Long term payables',
                         'H-Other Payables or Accruals',
                         'H1-Deferred Revenue',
                         'J-Intra-Group or Inter-Company Balances',
                         'K-Sales Taxes',
                         'L-Taxation',
                         'M-Other Provisions for Liabilities',
                         'M1-Pensions',
                         'P(B/S)-Share Capital, Reserves and Dividends',
                         'P(I/S)-Share Capital, Reserves and Dividends',
                         'P1-Funds',
                         'Q-Revenue',
                         'Q1-Incoming resources',
                         'B1-Endowment Assets',
                         'H2-Deferred Capital Grants',
                         'Q2-HEFCE_TDA grant income',
                         'Q3-Tuition fee income',
                         'Q4-Research grant and contracts',
                         'Q5-Other Income',
                         'Q6-Endowment and investment income',
                         'R-Cost of Sales',
                         'R1-Resources expended',
                         'R2-Expenses',
                         'S-Payroll Expenses',
                         'T-Overheads or other profit and loss account items',
                         'T1-Interest Received',
                         'T2-Interest Paid',
                         'T3-Taxation Charge',
                         'T4-Other Income and Expenditure',
                         'T5-Net gain_loss on hedging instrument',
                         'T6-Fee and commission income',
                         'OTHER-OTHER',
                         'CC-Financial Statement Preparation',
                         'JNL-Journals',
                         'DD-Subsequent Events',
                         'GG-Going Concern',
                         'JJ-Consolidation',
                         'NN-Contingencies Commitments',
                         'VV-Related Party Transactions',
                         'YY-Derivatives',
                         'CF-Cash Flow Statement'
                         ]

        # ================== 0.0 - Top Frame ==================
        self.top_frame = tk.Frame(master)
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.master.add(self.top_frame, text='COA Regeneration')
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(1, weight=1)

        # self.master.tab(3, state="disabled")

        # ================== 1.0 - Load Mappings ==================
        self.load_frame = tk.Frame(self.top_frame)
        self.load_frame.grid(row=0, column=0, sticky='NSEW')
        self.load_frame.columnconfigure(0, weight=1)

        self.load_label = tk.Label(self.load_frame, text='Select Mapping options & load COA')
        self.load_label.grid(row=0, column=0, sticky='NSEW')

        # Case - Variable
        self.coa_var = tk.IntVar()
        # Upper - Radio Button
        self.coa_isolate = tk.Radiobutton(self.load_frame, text='Map COA from source TB',
                                          variable=self.coa_var, value=0)
        self.coa_isolate.grid(row=1, column=0, sticky='W')
        # Lower - Radio Button
        self.coa_extend = tk.Radiobutton(self.load_frame, text='Extend mappings to all TBs',
                                         variable=self.coa_var, value=1)
        self.coa_extend.grid(row=2, column=0, sticky='W')
        self.coa_map = tk.Button(self.load_frame, text='Map Chart of Accounts', command=self.load_coa)
        self.coa_map.grid(row=3, column=0, sticky='EW')

        self.warning_frame = tk.Frame(self.top_frame)
        self.warning_frame.grid(row=0, column=1, sticky='NSEW')
        self.warn_label = tk.Label(self.warning_frame)
        self.warn_label.grid(row=0, column=0, sticky='W')

        # ================== 2.0 - Load FSA options ==================

        self.options_frame = tk.Frame(self.top_frame)
        self.options_frame.grid(row=1, column=0, sticky='NSEW')
        self.options_frame.columnconfigure(0, weight=1)

        # ================== 2.1 - Results Frame ==================

        self.results_frame = tk.Frame(self.options_frame)
        self.results_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)
        for x in range(2):
            self.results_frame.columnconfigure(x, weight=1)

        # Display labels
        self.coa_total_codes_label = tk.Label(self.results_frame, text='Total Mapped Codes:')
        self.coa_total_codes_label.grid(row=0, column=0, sticky='W')
        self.coa_total_codes = tk.Label(self.results_frame, text='-')
        self.coa_total_codes.grid(row=0, column=1, sticky='W')
        self.coa_mapped_codes_label = tk.Label(self.results_frame, text='Total Unmapped Codes:')
        self.coa_mapped_codes_label.grid(row=1, column=0, sticky='W')
        self.coa_mapped_codes = tk.Label(self.results_frame, text='-')
        self.coa_mapped_codes.grid(row=1, column=1, sticky='W')
        self.coa_non_standard_label = tk.Label(self.results_frame, text='Total Non-Standard FSA:')
        self.coa_non_standard_label.grid(row=2, column=0, sticky='W')
        self.coa_non_standard = tk.Label(self.results_frame, text='-')
        self.coa_non_standard.grid(row=2, column=1, sticky='W')

        # ================== 2.2 - Automap Frame ==================
        self.automap_frame = tk.Frame(self.options_frame)
        self.automap_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        self.automap_frame.columnconfigure(0, weight=1)

        # Case - Variable
        self.map_var = tk.IntVar()
        # No adjustments - Radio Button
        self.map_isolate = tk.Radiobutton(self.automap_frame, text='Maintain non-standard FSAs',
                                          variable=self.map_var, value=0)
        self.map_isolate.grid(row=0, column=0, sticky='W')
        # Approximate Mapping - Radio Button
        self.map_isolate = tk.Radiobutton(self.automap_frame, text='Approx. Mapping',
                                          variable=self.map_var, value=1)
        self.map_isolate.grid(row=1, column=0, sticky='W')

        self.map_button = tk.Button(self.automap_frame, text='Auto-Map non-standard FSAs',
                                    command=self.automap_fsa
                                    )
        self.map_button.grid(row=2, column=0, sticky='EW')

        # ================== 3.0 - Main Canvas Frame ==================
        self.can_frame = tk.LabelFrame(self.top_frame)
        self.can_frame.grid(row=1, column=1, sticky='NSEW')
        for x in range(2):
            self.can_frame.columnconfigure(x, weight=1)
        self.can_frame.rowconfigure(1, weight=1)
        # ================== 3.1 - Header Canvas Frame ==================
        # Header Canvas
        self.head_can = tk.Canvas(self.can_frame, height=23)
        self.head_can.grid(row=0, column=0, columnspan=2, sticky='EW')
        self.head_can.bind('<Configure>', self.frame_width)
        # Header Canvas Sub-Frame
        self.head_can_sub_frame = tk.Frame(self.head_can)
        self.head_can_sub_frame.bind('<Configure>', self.config_frame)
        # Header canvas Window
        self.head_can_window = self.head_can.create_window(0, 0, anchor='nw', window=self.head_can_sub_frame)
        # Header Canvas Labels
        self.head_label = tk.Label(self.head_can_sub_frame, text='TB File')
        self.head_label.grid(row=0, column=0)
        # Header Canvas - Column Headers
        for x, header in zip(range(2), ['Account Code', 'Descriptions']):
            tk.Label(self.head_can_sub_frame, text=header).grid(row=0, column=x)
            self.head_can_sub_frame.columnconfigure(x, weight=1)

        # ================== 3.2 - Data Canvas Frame ==================
        self.data_can = tk.Canvas(self.can_frame, bg='#BDCDFF')
        self.data_can.grid(row=1, column=0, columnspan=2, sticky='NSEW')
        self.data_can.bind('<Configure>', self.frame_width)
        self.data_can.rowconfigure(0, weight=1)
        # Main Canvas Sub-Frame
        self.data_can_sub_frame = tk.Frame(self.data_can)
        for col in range(2):
            self.data_can_sub_frame.columnconfigure(col, weight=1)
        self.data_can_sub_frame.bind('<Configure>', self.config_frame)
        # Main Canvas Window
        self.data_can_window = self.data_can.create_window(0, 0, anchor='nw', window=self.data_can_sub_frame)
        # Scrollbar
        self.data_can_scroll = tk.Scrollbar(self.can_frame, orient="vertical", command=self.data_can.yview)
        self.data_can_scroll.grid(row=1, column=3, sticky='NS')

        # ================== 4.0 - Save COA Mapping ==================
        self.save_coa_frame = tk.Label(self.top_frame)
        self.save_coa_frame.grid(row=2, column=0, sticky='NSEW')
        self.save_coa_frame.columnconfigure(0, weight=1)

        # Check mappings button
        self.replace_desc_button = tk.Button(self.save_coa_frame, text='Check & Save Mappings:', height=3,
                                             command=self.save_mappings
                                             )
        self.replace_desc_button.grid(row=0, column=0, sticky='EW')

        self.save_coa_frame_2 = tk.Frame(self.top_frame)
        self.save_coa_frame_2.grid(row=2, column=1, sticky='NSEW')
        self.save_coa_frame_2.columnconfigure(0, weight=1)
        self.save_coa_frame_2.rowconfigure(0, weight=1)

        self.save_coa_label = tk.Label(self.save_coa_frame_2, text='', anchor='w')
        self.save_coa_label.grid(row=0, column=0, sticky='NSW')

        self.disable_children(self.automap_frame)
        self.disable_children(self.save_coa_frame)
        self.disable_children(self.warning_frame)
        self.disable_children(self.can_frame)

    # region Canvas Display Functions
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

    def frame_width(self, event):
        # Updates widths of main and header canvas when adjusted to fit window
        canvas_width = event.width
        event.widget.itemconfigure(self.data_can_window, width=canvas_width)

    # endregion

    # region Enable/Disable Canvas Functions
    def enable_children(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            print(child)
            widget_type = child.winfo_class()
            if widget_type not in ('Frame', 'Labelframe', 'Scrollbar'):
                child.configure(state='normal')
            else:
                # 2) Repeats loops with sub_children of widget
                self.enable_children(child)

    def disable_children(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            widget_type = child.winfo_class()
            if widget_type not in ('Frame', 'Labelframe', 'Scrollbar'):
                child.configure(state='disable')
            else:
                # 2) Repeats loops with sub_children of widget
                self.disable_children(child)

    # endregion

    def load_coa(self):
        desc_check = self.main.desc_accepted
        raw_coa = self.main.raw_coa.copy()

        if desc_check:
            # 1) Add unique field to raw COA
            raw_coa['Unique'] = raw_coa['Filename'].astype(str) + raw_coa['Code'].astype(str)
            # print('============== RAW COA MAPPING ================')
            # print(raw_coa)

            # 2) Create new COA, add unique field
            code_field = 'Pref. Code' if self.main.prefix_on else 'Code'
            if self.main.prefix_on:
                keep_fields = ['Filename', 'Code', 'Pref. Code', 'Desc. New']
            else:
                keep_fields = ['Filename', 'Code', 'Desc. New']

            coa = self.main.final_tb[keep_fields].copy()
            # CAUSES ERRORS WITH MULTIPLE CODES FROM DIFFERENT FILES DUE TO FIRST PRIORITY, FILTERS OUT MAPPINGS
            coa.drop_duplicates([code_field, 'Desc. New'], inplace=True)

            # 3) Combine on different fields depending on if prefixes were selected or not
            coa['Unique'] = coa['Filename'].astype(str) + coa['Code'].astype(str)
            coa.drop_duplicates(['Unique'], inplace=True)  # <<<<<< MAY BREAK SCRIPT
            raw_coa.drop_duplicates(['Unique'], inplace=True)  # <<<<<< MAY BREAK SCRIPT
            coa = pd.merge(coa, raw_coa[['Unique', 'FSA']], on='Unique', how='left')

            # 4) Extend FSA mappings to other files where found (updated 12/06/22 to used)
            if self.coa_var.get() == 1:
                raw_coa.drop_duplicates(['Code'], inplace=True)  # <<<<<< MAY BREAK SCRIPT
                coa = pd.merge(coa, raw_coa[['Code', 'FSA']], on='Code', how='left', suffixes=('', ' Ext.'))
                coa['FSA Orig. + Ext.'] = coa['FSA'].where(coa['FSA'].notnull(), coa['FSA Ext.'])
            else:
                coa['FSA Orig. + Ext.'] = coa['FSA']

            print(coa)

            self.coa = coa.copy()

            # 5) Get instances of none standard FSA's <<<<<<< ORIGINAL SCRIPT, USED FSA INSTEAD
            # FSA NOTES
            # fsa_flag = coa[~coa['FSA'].isin(self.fsa_list)].copy()
            # fsa_flag.drop(['Code', 'Desc. New'], axis=1, inplace=True)
            # fsa_flag = fsa_flag[fsa_flag['FSA'].notnull()]
            # fsa_flag = fsa_flag['FSA'].unique().tolist()
            # fsa_flag.sort(key=str.lower)
            # print('============== FSA NONE STANDARD FLAG ================')
            # print(fsa_flag)

            # 5) Get instances of none standard FSA's
            fsa_flag = coa[~coa['FSA Orig. + Ext.'].isin(self.fsa_list)].copy()
            fsa_flag.drop(['Code', 'Desc. New'], axis=1, inplace=True)
            fsa_flag = fsa_flag[fsa_flag['FSA Orig. + Ext.'].notnull()]
            fsa_flag = fsa_flag['FSA Orig. + Ext.'].unique().tolist()
            fsa_flag.sort(key=str.lower)

            # 6) Generate GUI is no. of FSA's if below threshold, otherwise set fsa_limit to true
            for widgets in self.data_can_sub_frame.winfo_children():
                widgets.destroy()

            if len(fsa_flag) > 300:
                self.warn_label.config(text='No. of non-standard FSAs exceeds ' + str(len(fsa_flag)) +
                                            ', too large to display. FSA Mappings must be adjusted after export.')
                self.fsa_limit = True

                # DISABLE AUTO-MAPPING?
                self.enable_children(self.automap_frame)
                self.enable_children(self.save_coa_frame)
                self.enable_children(self.warning_frame)
                self.enable_children(self.can_frame)

            elif len(fsa_flag) == 0:
                self.warn_label.config(text='New COA has been generated. No non-standard FSAs found.')
                self.fsa_limit = False

                coa_local = self.coa.copy()
                coa_local['FSA New'] = coa_local['FSA Orig. + Ext.']
                self.main.final_coa = coa_local.copy()
                self.main.coa_accepted = True
                print('======= FINAL COA - NO ERRORS =======')
                print(self.main.final_coa)

                # DISABLE AUTO-MAPPING?
                self.disable_children(self.automap_frame)
                self.disable_children(self.save_coa_frame)
                self.disable_children(self.warning_frame)
                self.disable_children(self.can_frame)

            else:
                self.fsa_limit = False

                # ENABLE AUTOMAPPING?
                self.enable_children(self.automap_frame)
                self.enable_children(self.save_coa_frame)
                self.enable_children(self.warning_frame)
                self.enable_children(self.can_frame)

                for x in fsa_flag:
                    y = fsa_flag.index(x)

                    # Insert non-standard description into entry
                    fsa = tk.Entry(self.data_can_sub_frame)
                    fsa.insert(0, x)
                    fsa.grid(row=y, column=0, sticky='EW')
                    fsa.config(state='readonly')

                    # Add non-standard FSA to potential mappings list
                    fsa_options = self.fsa_list.copy()
                    fsa_options.append(x)
                    fsa_options.sort(key=str.lower)

                    # Mapping option combobox
                    multiple_desc = ttk.Combobox(self.data_can_sub_frame, values=fsa_options)
                    multiple_desc.grid(row=y, column=1, sticky='EW')
                    multiple_desc.current(fsa_options.index(x))

            # Update GUI code listings
            self.coa_total_codes.config(text=coa[code_field].nunique())
            self.coa_mapped_codes.config(text=coa['FSA Orig. + Ext.'].isna().sum())
            self.coa_non_standard.config(text=len(fsa_flag))

            self.warn_label.config(text='New COA has been generated. Please review any non-standard mappings.')

        else:
            self.warn_label.config(text='Description mappings have not been approved in previous tab. Please revise.')

    def automap_fsa(self):
        widgets = self.data_can_sub_frame.winfo_children()
        widget_list = [widgets[y:y + 2] for y in range(0, len(widgets), 2)]

        print(widget_list)

        row: list
        if self.map_var.get() == 0:
            for row in widget_list:
                row[1].set(row[0].get())

        if self.map_var.get() == 1:
            for row in widget_list:
                # Get current mapping in lower case
                fsa_old = row[0].get()

                # print(str(fsa_old) + ' - Searching')
                for x in range(3, -1, -1):
                    # print(str(fsa_old) + ' - string length: ' + str(x) + ' - ' + str(fsa_old[:x].lower().strip()))
                    for fsa in self.fsa_list:
                        if x == 0:
                            # print(fsa_old)
                            row[1].set(fsa_old)
                            # print('\n')
                            break
                        elif fsa_old[:x].lower().strip() == fsa[:x].lower().strip():
                            # print(fsa)
                            row[1].set(fsa)
                            # print('\n')
                            break
                    else:
                        continue
                    break

    def save_mappings(self):
        error_flag = False
        minor_flag = False
        # Check if new COA has been generated yet
        if self.coa.empty:
            self.save_coa_label.config(text='Please Map COA, FSAs have not been loaded')

        # Map COA to global final coa if mapping limit is reached
        elif self.fsa_limit:
            coa_local = self.coa.copy()
            coa_local['FSA New'] = coa_local['FSA Orig. + Ext.']
            self.main.final_coa = coa_local.copy()
            self.main.coa_accepted = True
            print('======= FINAL COA - NO GUI AUTOMAPPING DUE TO CODE LIMIT =======')
            print(self.main.final_coa)

        # Automap nonstandard FSA's to standardised codes using merge
        else:
            # 1) Generate list from tkinter canvas GUI
            widgets = self.data_can_sub_frame.winfo_children()
            widget_list = [widgets[y:y + 2] for y in range(0, len(widgets), 2)]
            print(widget_list)
            row: list
            new_mappings = [[row[0].get(), row[1].get()] for row in widget_list]

            # Check if any descriptions have been left unmapped
            for row in widget_list:
                print(row)
                if len(row[1].get()) == 0:
                    error_flag = True
                    row[0].config(readonlybackground='#ff684c')
                elif row[1].get() in self.fsa_list:
                    row[0].config(readonlybackground='#8ace7e')
                else:
                    row[0].config(readonlybackground='#ffda66')
                    minor_flag = True

            if not error_flag:
                # 2) Convert GUI list to dataframe
                join_df = pd.DataFrame(new_mappings, columns=['FSA Orig. + Ext.', 'FSA New'])
                print('JOINED DAA FRAME')
                print(join_df)

                # Merge COA with remapped none standard codes
                final_fsa = pd.merge(self.coa, join_df, on='FSA Orig. + Ext.', how='left')
                print(final_fsa)
                final_fsa['FSA New'].fillna(final_fsa['FSA Orig. + Ext.'], inplace=True)
                self.main.final_coa = final_fsa.copy()
                self.main.coa_accepted = True

                print('======= FINAL COA - REMAPPED NONE-STANDARDS =======')
                print(self.main.final_coa)

                if not minor_flag:
                    self.save_coa_label.config(text='COA Mappings saved.', fg='#8ace7e')
                else:
                    self.save_coa_label.config(text='COA Mappings saved. '
                                                    'NOTE: Some non-standard FSAs retained, '
                                                    'highlighted yellow.', fg='#8ace7e')

            else:
                self.save_coa_label.config(text='Blank FSA mappings highlighted, please select.')
                self.main.coa_accepted = False
