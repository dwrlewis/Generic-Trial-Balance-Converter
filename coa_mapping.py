import tkinter as tk
from tkinter import ttk
import pandas as pd


class CoaConfigure:
    def __init__(self, master, main):
        self.master = master
        self.main = main

        # region Variables
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
        # endregion

        # region ================== 0.0 - Top Frame ==================
        self.top_frame = tk.Frame(master)
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.master.add(self.top_frame, text='COA Regeneration')
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        # self.master.tab(3, state="disabled")
        # endregion

        # region ================== 1.0 - Load Mappings ==================
        # Load Mappings Header Frame and Label
        self.load_frame = tk.Frame(self.top_frame)
        self.load_frame.grid(row=0, column=0, sticky='NSEW')
        self.load_frame.columnconfigure(0, weight=1)
        self.load_label = tk.Label(self.load_frame, text='Select COA Mapping Sources:')
        self.load_label.grid(row=0, column=0, sticky='W')
        # Set COA Source Radio Buttons
        self.coa_var = tk.IntVar()
        self.load_isolate = tk.Radiobutton(self.load_frame, text='Source TB Only', variable=self.coa_var, value=0)
        self.load_isolate.grid(row=1, column=0, sticky='W')
        self.load_extend = tk.Radiobutton(self.load_frame, text='Extend to all TBs', variable=self.coa_var, value=1)
        self.load_extend.grid(row=2, column=0, sticky='W')
        self.load_map = tk.Button(self.load_frame, text='Map Chart of Accounts', command=self.load_coa)
        self.load_map.grid(row=3, column=0, sticky='EW')
        # Warning Frame and Label
        self.save_warn_frame = tk.Frame(self.top_frame)
        self.save_warn_frame.grid(row=0, column=1, sticky='NSEW')
        self.load_warn_label = tk.Label(self.save_warn_frame)
        self.load_warn_label.grid(row=0, column=0, sticky='W')
        # endregion

        # region ================== 2.0 - Load FSA options ==================

        self.options_frame = tk.Frame(self.top_frame)
        self.options_frame.grid(row=1, column=0, sticky='NSEW')
        self.options_frame.columnconfigure(0, weight=1)

        # region ================== 2.1 - Results Frame ==================
        self.result_frame = tk.Frame(self.options_frame)
        self.result_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)
        for x in range(2):
            self.result_frame.columnconfigure(x, weight=1)
        # Display labels for COA mappings
        self.result_label_map = tk.Label(self.result_frame, text='Total Mapped Codes:')
        self.result_label_map.grid(row=0, column=0, sticky='W')
        self.result_mapped = tk.Label(self.result_frame, text='-')
        self.result_mapped.grid(row=0, column=1, sticky='W')
        self.result_label_unmap = tk.Label(self.result_frame, text='Total Unmapped Codes:')
        self.result_label_unmap.grid(row=1, column=0, sticky='W')
        self.result_unmapped = tk.Label(self.result_frame, text='-')
        self.result_unmapped.grid(row=1, column=1, sticky='W')
        self.result_label_misc = tk.Label(self.result_frame, text='Total Non-Standard FSA:')
        self.result_label_misc.grid(row=2, column=0, sticky='W')
        self.result_misc = tk.Label(self.result_frame, text='-')
        self.result_misc.grid(row=2, column=1, sticky='W')
        # endregion

        # region ================== 2.2 - Automap Frame ==================
        self.map_frame = tk.Frame(self.options_frame)
        self.map_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        self.map_frame.columnconfigure(0, weight=1)
        # Original/Approximate Mappings Radio Buttons
        self.map_var = tk.IntVar()
        self.map_ori = tk.Radiobutton(self.map_frame, text='Maintain non-standard FSAs', variable=self.map_var, value=0)
        self.map_ori.grid(row=0, column=0, sticky='W')
        self.map_approx = tk.Radiobutton(self.map_frame, text='Approx. Mapping', variable=self.map_var, value=1)
        self.map_approx.grid(row=1, column=0, sticky='W')
        # Map FSAs
        self.map_button = tk.Button(self.map_frame, text='Auto-Map non-standard FSAs', command=self.automap_fsa)
        self.map_button.grid(row=2, column=0, sticky='EW')
        # endregion

        # endregion

        # region ================== 3.0 - Main Canvas Frame ==================
        self.can_frame = tk.LabelFrame(self.top_frame)
        self.can_frame.grid(row=1, column=1, sticky='NSEW')
        for x in range(2):
            self.can_frame.columnconfigure(x, weight=1)
        self.can_frame.rowconfigure(1, weight=1)

        # region ================== 3.1 - Header Canvas Frame ==================
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
        # endregion

        # region ================== 3.2 - Data Canvas Frame ==================
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
        # endregion

        # endregion

        # region ================== 4.0 - Save COA Mapping ==================
        self.save_frame = tk.Label(self.top_frame)
        self.save_frame.grid(row=2, column=0, sticky='NSEW')
        self.save_frame.columnconfigure(0, weight=1)
        # Save FSA mappings Button
        self.save_button = tk.Button(self.save_frame, text='Check & Save Mappings:', height=3, command=self.save_map)
        self.save_button.grid(row=0, column=0, sticky='EW')
        # Display output errors
        self.save_warn_frame = tk.Frame(self.top_frame)
        self.save_warn_frame.grid(row=2, column=1, sticky='NSEW')
        self.save_warn_frame.columnconfigure(0, weight=1)
        self.save_warn_frame.rowconfigure(0, weight=1)
        self.save_warn_label = tk.Label(self.save_warn_frame, text='', anchor='w')
        self.save_warn_label.grid(row=0, column=0, sticky='NSW')
        # endregion

        # self.disable_children(self.automap_frame)
        # self.disable_children(self.save_coa_frame)
        # self.disable_children(self.warning_frame)
        # self.disable_children(self.can_frame)

    # region 1.0 - Load COA
    def load_coa(self):
        # region 1) Assign master variables to local for readability
        desc_check = self.main.desc_accepted
        raw_coa = self.main.raw_coa.copy()
        final_tb = self.main.final_tb.copy()
        # endregion

        # region 2) Check description tab has been completed
        if desc_check:
            # region 3) Add unique field to raw COA to filter for unique codes isolated by file
            raw_coa.drop_duplicates(subset=['Filename', 'Code'], inplace=True)
            print('1) Raw TB*')
            print(raw_coa)
            # endregion

            # region 4) Generate new COA from TB data with corrected descriptions
            coa = final_tb.copy()
            code_field = 'Pref. Code' if self.main.prefix_on else 'Code'
            coa.drop_duplicates(subset=[code_field, 'Filename', 'Desc. New'], inplace=True)
            print('2) coa with dupes from code_field, Filename, Desc. New dropped*')
            print(coa)
            # endregion

            # region 5) Combine on different fields depending on if prefixes were selected or not
            coa = pd.merge(coa, raw_coa[['Filename', 'Code', 'FSA']], on=['Filename', 'Code'], how='left')
            print('3) Merged COA on Filename & Code*')
            print(coa)
            # endregion

            # region 6) Extend FSA mappings to other files where no mappings in source file, save to self COA
            if self.coa_var.get() == 1:
                raw_coa.drop_duplicates(['Code'], inplace=True)
                coa = pd.merge(coa, raw_coa[['Code', 'FSA']], on='Code', how='left', suffixes=('', ' Ext.'))
                coa['FSA'] = coa['FSA'].where(coa['FSA'].notnull(), coa['FSA Ext.'])
            print('4) COA with extensions to mappings')
            print(coa)

            self.coa = coa[[code_field, 'Desc. New', 'FSA']].copy()
            print('5) COA with final fields')
            print(self.coa)

            # endregion

            # region 7) Get instances of non-standard FSA's in new COA
            fsa_flag = coa[~coa['FSA'].isin(self.fsa_list)].copy()
            fsa_flag.drop([code_field, 'Desc. New'], axis=1, inplace=True)
            fsa_flag = fsa_flag[fsa_flag['FSA'].notnull()]
            fsa_flag = fsa_flag['FSA'].unique().tolist()
            fsa_flag.sort(key=str.lower)
            print('6) Inconsistent FSA flag')
            print(fsa_flag)
            # endregion

            # region 8) Destroy canvas widgets
            for widgets in self.data_can_sub_frame.winfo_children():
                widgets.destroy()
            # endregion

            # region 9) Generate canvas GUI if no. of FSA's if below threshold, otherwise set fsa_limit to true
            if len(fsa_flag) == 0:
                self.fsa_limit = False
                self.load_warn_label.config(text='New COA has been generated. No non-standard FSAs found.')
                self.main.final_coa = coa.copy()
                self.main.coa_accepted = True
                # DISABLE AUTO-MAPPING

            elif len(fsa_flag) <= 300:
                self.fsa_limit = False
                # ENABLE AUTOMAPPING
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
            else:
                self.fsa_limit = True
                self.load_warn_label.config(text='No. of non-standard mappings exceeds ' + str(len(fsa_flag)) +
                                            ', too large to display. Adjust manually after export.')
                # DISABLE AUTO-MAPPING
            # endregion

            # region 10) Update GUI code listings for no. of unmapped/irregular mappings
            self.result_mapped.config(text=coa[code_field].nunique())
            # self.coa_mapped_codes.config(text=coa['FSA Orig. + Ext.'].isna().sum())
            self.result_unmapped.config(text=coa['FSA'].isna().sum())
            self.result_misc.config(text=len(fsa_flag))
            self.load_warn_label.config(text='New COA has been generated. Please review any non-standard mappings.')
            # endregion

        else:
            self.load_warn_label.config(text='Desc. mappings have not been approved in previous tab. Please revise.')
        # endregion
    # endregion

    # region 2.0 - Automap COA
    def automap_fsa(self):
        widgets = self.data_can_sub_frame.winfo_children()
        widget_list = [widgets[y:y + 2] for y in range(0, len(widgets), 2)]
        row: list
        if self.map_var.get() == 0:
            for row in widget_list:
                row[1].set(row[0].get())

        if self.map_var.get() == 1:
            for row in widget_list:
                # Get current mapping in lower case
                fsa_old = row[0].get()
                for x in range(3, -1, -1):
                    for fsa in self.fsa_list:
                        if x == 0:
                            row[1].set(fsa_old)
                            break
                        elif fsa_old[:x].lower().strip() == fsa[:x].lower().strip():
                            row[1].set(fsa)
                            break
                    else:
                        continue
                    break
    # endregion

    # region 3.0 - Canvas Display Functions
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

    # region 4.0 - Save Mappings
    def save_map(self):
        error_flag = False
        minor_flag = False

        # region 1) Check if new COA has been generated yet
        if self.coa.empty:
            self.save_warn_label.config(text='Please Map COA, FSAs have not been loaded')
        # endregion

        # region 2) If inconsistent mappings exceeded GUI display limits used new COA with original mappings
        elif self.fsa_limit:
            self.main.final_coa = self.coa.copy()
            self.main.coa_accepted = True
        # endregion

        # region 3) If remapping of non-standard codes was selected apply new mappings
        else:
            # region 3.1) Generate mapping array from tkinter canvas GUI
            widgets = self.data_can_sub_frame.winfo_children()
            widget_list = [widgets[y:y + 2] for y in range(0, len(widgets), 2)]
            new_mappings = [[row[0].get(), row[1].get()] for row in widget_list]
            # endregion

            # region 3.2) Check if any descriptions have been left unmapped
            row: list
            for row in widget_list:
                # if len(row[1].get()) == 0:
                #     error_flag = True
                #     row[0].config(readonlybackground='#ff684c')
                # elif row[1].get() in self.fsa_list:
                #     row[0].config(readonlybackground='#8ace7e')
                # else:
                #     row[0].config(readonlybackground='#ffda66')
                #     minor_flag = True

                fsa = row[1].get()
                colour = '#ff684c' if len(fsa) == 0 else '#8ace7e' if fsa in self.fsa_list else '#ffda66'
                if not error_flag:
                    error_flag = True if len(fsa) == 0 else False
                if not minor_flag:
                    minor_flag = True if fsa in self.fsa_list else False
                row[0].config(readonlybackground=colour)
            # endregion

            # region 3.3) Standardise mappings based on selections
            if not error_flag:
                # Convert GUI selections to dataframe
                join_df = pd.DataFrame(new_mappings, columns=['FSA', 'FSA Remap'])
                # Join new code mappings onto regenerated COA
                final_fsa = pd.merge(self.coa, join_df, on='FSA', how='left')
                final_fsa['FSA Remap'].fillna(final_fsa['FSA'], inplace=True)
                # Update GUI comment
                if not minor_flag:
                    self.save_warn_label.config(text='FSAs saved.', fg='#8ace7e')
                else:
                    self.save_warn_label.config(text='FSAs saved. NOTE: Non-standard FSAs retained, shown in yellow.',
                                                fg='#8ace7e')
                # Update master final COA
                self.main.final_coa = final_fsa.copy()
                self.main.coa_accepted = True
                print('7) Remapped FSA')
                print(final_fsa)
            else:
                self.save_warn_label.config(text='Blank FSA mappings highlighted, please select.')
                self.main.coa_accepted = False
            # endregion
        # endregion
    # endregion

    # region Misc. - Enable/Disable Canvas Functions
    def enable_children(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
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
