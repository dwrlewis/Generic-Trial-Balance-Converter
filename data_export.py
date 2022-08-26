import tkinter as tk
import pandas as pd
import os
from tkinter import filedialog


class DataExport:
    def __init__(self, master, main):
        self.master = master
        self.main = main

        # region Variables
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
        self.master.add(self.top_frame, text='Export Data')
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        # endregion

        # region ================== 1.0 - Check Data & Options ==================
        self.check_frame = tk.Frame(self.top_frame)
        self.check_frame.grid(row=0, rowspan=2, column=0, sticky='NSEW')

        self.check_data = tk.Button(self.check_frame, text='Review Data:', command=self.check_data, height=2)
        self.check_data.grid(column=0, sticky='EW')

        # TB Export Options
        tk.Label(self.check_frame, text='Trial Balance Exports:', pady=6).grid(column=0, sticky='W')
        self.tb_opt_list = []
        self.tb_opt_var_list = []
        for y, tb in enumerate(['Adjusted TB', 'Raw TB', 'Detailed Meta TB']):
            tb_var = tk.IntVar(value=0)
            tb_check = tk.Checkbutton(self.check_frame, text=tb, variable=tb_var, state='disabled')
            tb_check.grid(column=0, sticky='W')
            self.tb_opt_list.append(tb_check)
            self.tb_opt_var_list.append(tb_var)

        # COA Export Options
        tk.Label(self.check_frame, text='COA Exports:', pady=6).grid(column=0, sticky='W')
        self.coa_opt_list = []
        self.coa_opt_var_list = []
        for y, tb in enumerate(['Adjusted COA', 'Raw COA', 'Detailed Meta COA']):
            coa_var = tk.IntVar(value=0)
            coa_check = tk.Checkbutton(self.check_frame, text=tb, variable=coa_var, state='disabled')
            coa_check.grid(column=0, sticky='W')
            self.coa_opt_list.append(coa_check)
            self.coa_opt_var_list.append(coa_var)

        # COA Filter unmapped FSA's option
        self.coa_label = tk.Label(self.check_frame, text='Options:', pady=6)
        self.coa_label.grid(column=0, sticky='W')

        self.coa_unmap_var = tk.IntVar(value=0)
        self.coa_unmap_check = tk.Checkbutton(self.check_frame, text='Drop blank FSAs?',
                                              variable=self.coa_unmap_var, state='disabled')
        self.coa_unmap_check.grid(column=0, sticky='W')
        # endregion

        # region ================== 2.0 - TB Data Check ==================
        self.tb_dqi_frame = tk.Frame(self.top_frame)
        self.tb_dqi_frame.grid(row=0, column=1, sticky='NSEW')
        for x in range(1, 3):
            self.tb_dqi_frame.columnconfigure(x, weight=1)

        # TB X axis Headers
        tb_x_string = ['Line Count:', 'Unique Companies:']
        for x, string in enumerate(tb_x_string):
            tk.Label(self.tb_dqi_frame, text=string).grid(row=0, column=x + 1, padx=3, pady=3)

        # TB Y Axis Headers
        tb_y_string = ['PY', 'OP', 'CL', 'Raw TB Totals', '', 'Prefixed', '', 'Desc. Checked', '', 'Adj. TB Totals']
        for y, string in enumerate(tb_y_string):
            tk.Label(self.tb_dqi_frame, text=string, width=12).grid(row=y + 1, column=0, padx=3, pady=3)
            if string != '':
                self.tb_dqi_frame.rowconfigure(y + 1, weight=1)

        # TB Raw Line & Company Amounts/Total
        self.raw_tb_entries = []
        for y in range(1, 5):
            self.lines_entry = tk.Entry(self.tb_dqi_frame, width=8, justify='center')
            self.lines_entry.grid(row=y, column=1, sticky='NSEW', padx=3, pady=3)

            self.comp_entry = tk.Entry(self.tb_dqi_frame, justify='center')
            self.comp_entry.grid(row=y, column=2, sticky='NSEW', padx=3, pady=3)

            self.raw_tb_entries.append([self.lines_entry, self.comp_entry])

        # TB Adjustment Checks
        self.settings = []
        self.adj_tb_entries = []
        for y in range(5, 10, 2):
            tk.Label(self.tb_dqi_frame, text=' ˅ ').grid(row=y, column=1, columnspan=2, sticky='NSEW')
            if y < 9:
                tb_settings_entry = tk.Entry(self.tb_dqi_frame, justify='center')
                tb_settings_entry.grid(row=y + 1, column=1, columnspan=2, sticky='NSEW', padx=3, pady=3)
                self.settings.append(tb_settings_entry)

        # TB adjusted Line & Company Amounts/Total
        self.adj_lines_entry = tk.Entry(self.tb_dqi_frame, justify='center')
        self.adj_lines_entry.grid(row=10, column=1, sticky='NSEW', padx=3, pady=3)
        self.adj_comp_entry = tk.Entry(self.tb_dqi_frame, justify='center')
        self.adj_comp_entry.grid(row=10, column=2, sticky='NSEW', padx=3, pady=3)

        # endregion

        # region ================== 3.0 - COA Data Check ==================
        self.coa_dqi_frame = tk.Frame(self.top_frame)
        self.coa_dqi_frame.grid(row=1, column=1, sticky='NSEW')

        # COA X axis Headers
        tb_x_string = ['Unique Codes', 'Irregular FSAs', 'Blank FSAs']
        for x, string in enumerate(tb_x_string):
            tk.Label(self.coa_dqi_frame, text=string).grid(row=0, column=x + 1, padx=3, pady=3)
            if string != '':
                self.coa_dqi_frame.columnconfigure(x + 1, weight=1)

        # COA Y Axis Headers
        tb_y_string = ['Raw COA', '', 'New COA?', '', 'Adj. COA']
        for y, string in enumerate(tb_y_string):
            tk.Label(self.coa_dqi_frame, text=string, width=12).grid(row=y + 1, column=0, padx=3, pady=3)
            if string != '':
                self.coa_dqi_frame.rowconfigure(y + 1, weight=1)

        # COA Raw Line & FSA amounts
        self.raw_coa_entries = []
        for x in range(3):
            entry = tk.Entry(self.coa_dqi_frame, justify='center')
            entry.grid(row=1, column=x + 1, sticky='NSEW', padx=3, pady=3)
            self.raw_coa_entries.append(entry)

        # COA Regeneration Check
        tk.Label(self.coa_dqi_frame, text=' ˅ ').grid(row=2, column=1, columnspan=3, sticky='NSEW')
        self.coa_check_entry = tk.Entry(self.coa_dqi_frame, justify='center')
        self.coa_check_entry.grid(row=3, column=1, columnspan=3, sticky='NSEW', padx=5, pady=3)
        self.settings.append(self.coa_check_entry)
        tk.Label(self.coa_dqi_frame, text=' ˅ ').grid(row=4, column=1, columnspan=3, sticky='NSEW')

        # COA Adj Line & FSA amounts
        self.adj_coa_entries = []
        for x in range(3):
            entry = tk.Entry(self.coa_dqi_frame, justify='center')
            entry.grid(row=5, column=x + 1, sticky='NSEW', padx=3, pady=3)
            self.adj_coa_entries.append(entry)

        # endregion

        # region ================== 4.0 - Export Path ==================
        # Select FP button
        self.export_button_frame = tk.Frame(self.top_frame)
        self.export_button_frame.grid(row=2, column=0, sticky='EW')
        self.export_button_frame.columnconfigure(0, weight=1)

        self.fp_button = tk.Button(self.export_button_frame, text='Open:', command=self.export_path, height=3)
        self.fp_button.grid(row=0, column=0, sticky='EW')

        # Export fp & button
        self.export_fp_frame = tk.Frame(self.top_frame)
        self.export_fp_frame.grid(row=2, column=1, sticky='EW')
        self.export_fp_frame.columnconfigure(0, weight=1)

        self.fp_label = tk.Label(self.export_fp_frame, text='Select Export Directory')
        self.fp_label.grid(row=0, column=0, sticky='W')

        self.export_button = tk.Button(self.export_fp_frame, text='Export Data', command=self.data_export, height=3)
        self.export_button.grid(row=0, column=1, sticky='EW')
        # endregion

    # region Check Imported & Transformed Data, Reset GUI values displayed
    def check_data(self):

        # region 1) Clear all TB Period widgets & disable all export checks
        self.reset(self.tb_dqi_frame)
        self.reset(self.coa_dqi_frame)
        for child in self.check_frame.winfo_children():
            if child.winfo_class() == 'Checkbutton':
                child: tk.Checkbutton  # Prevents false flag pycharm error flags
                child.config(fg='#FFFFFF', state='disabled')

        pref_on = self.main.prefix_on
        pref_accept = self.main.prefix_accepted

        desc_on = self.main.desc_on
        desc_accept = self.main.desc_accepted

        coa_accept = self.main.coa_accepted
        # endregion

        # region 2) Raw TB Check for line total & unique companies by period, update GUI
        raw_tb = self.main.raw_tb
        if len(raw_tb) != 0:
            # Populate entries split by period
            for period, widget in zip(['Prior TB', 'Opening TB', 'Closing TB'], self.raw_tb_entries[:3]):
                # Lines for each period
                lines = raw_tb[raw_tb['TB Period'] == period]
                widget[0].insert(0, str(len(lines)))
                # Companies for each period
                companies = lines['Company'].unique().tolist()
                widget[1].insert(0, str(len(companies)))
            self.raw_tb_entries[3][0].insert(0, str(len(raw_tb)))
            self.raw_tb_entries[3][1].insert(0, str(len(set(raw_tb['Company'].unique().tolist()))))
            self.tb_opt_list[1].config(state='normal', fg='#8ace7e')
        else:
            for widget in self.raw_tb_entries:
                widget[0].insert(0, 'NULL')
                widget[1].insert(0, 'NULL')
        # endregion

        # region 3) Raw COA Check for line total, no. of irregular mappings, and blank mappings, update GUI
        raw_coa = self.main.raw_coa
        coa_lines, coa_irregular, coa_blank = self.raw_coa_entries
        if len(raw_coa) != 0:
            coa_lines.insert(0, str(len(raw_coa['Code'].unique())))
            coa_irregular.insert(0, str(len(raw_coa[~raw_coa['FSA'].isin(self.fsa_list)].dropna(subset=['FSA']))))
            coa_blank.insert(0, str(raw_coa['FSA'].isnull().sum()))
            self.coa_opt_list[1].config(state='normal', fg='#8ace7e')
        else:
            for widget in self.raw_coa_entries:
                widget.insert(0, 'NULL')
        # endregion

        # region 4) Settings Check, prefix, description & coa GUI update
        adj_list = [[pref_on, pref_accept],
                    [desc_on, desc_accept],
                    [desc_on, coa_accept]]

        for [adj_on, adj_complete], widget in zip(adj_list, self.settings):
            desc_colour = '#ffda66' if not adj_on else '#8ace7e' if adj_complete else '#ff684c'
            desc_text = 'Not Checked' if not adj_on else 'Complete' if adj_complete else 'Error'
            widget.insert(0, desc_text)
            widget.config(bg=desc_colour)
        # endregion

        # region 5) Adj TB Check for line total & unique companies by period, update GUI
        # Assign TB based on settings
        if desc_on and desc_accept:
            tb = self.main.final_tb.copy()
        elif pref_on and pref_accept:
            tb = self.main.prefixed_tb.copy()
        else:
            tb = self.main.raw_tb.copy()

        # Update adjusted TB lines & unique companies GUI
        if len(tb) != 0:
            self.adj_lines_entry.insert(0, str(len(tb)))
            comp_field = 'Company New' if pref_on and pref_accept else 'Company'
            self.adj_comp_entry.insert(0, str(len(tb[comp_field].unique().tolist())))
            self.tb_opt_list[0].config(state='normal', fg='#8ace7e')
            self.tb_opt_list[2].config(state='normal', fg='#8ace7e')
        else:
            self.adj_lines_entry.insert(0, 'NULL')
            self.adj_comp_entry.insert(0, 'NULL')
        # endregion

        # region 6) Adj COA Check for line total, no. of irregular mappings, and blank mappings, update GUI
        if self.main.desc_on and self.main.desc_accepted:
            coa = self.main.final_coa.copy()
            code = 'Pref. Code' if 'Pref. Code' in coa else 'Code'
            fsa_field = 'FSA Remap' if 'FSA Remap' in coa else 'FSA'
            lines, irregular, blank = self.adj_coa_entries

            if len(coa) != 0:
                lines.insert(0, str(len(coa[code].unique())))
                blank.insert(0, str(coa[fsa_field].isnull().sum()))
                irregular.insert(0, str(len(coa[~coa[fsa_field].isin(self.fsa_list)].dropna(subset=[fsa_field]))))
                self.coa_opt_list[0].config(state='normal', fg='#8ace7e')
                self.coa_opt_list[2].config(state='normal', fg='#8ace7e')
                self.coa_unmap_check.config(state='normal', fg='#8ace7e')
            else:
                for widget in self.adj_coa_entries:
                    widget.insert(0, 'NULL')
        else:
            for widget in self.adj_coa_entries:
                widget.insert(0, 'NULL')
        # endregion

    def reset(self, parent):
        for child in parent.winfo_children():
            widget_type = child.winfo_class()
            if widget_type == 'Entry':
                child.delete(0, tk.END)
            else:
                self.reset(child)
    # endregion

    # region Filepath selection & data export
    def export_path(self):
        try:
            fp = filedialog.askdirectory(initialdir='/', title='Select a directory')
            # Sets GUI label to selected filepath, exits function if not selected
            if len(fp) != 0:
                self.export_button['state'] = 'normal'
                self.fp_label.config(text=str(fp), fg='#8ace7e')
                os.chdir(fp)
            else:
                self.fp_label.config(text='ERROR: No Filepath was selected', fg='#ff684c')
                self.export_button['state'] = 'disable'
                return
        # Filepath error handling exception
        except Exception as error:
            self.fp_label.config(text='ERROR: ' + str(error), fg='#ff684c')
            self.export_button['state'] = 'disable'

    def data_export(self):
        try:
            with pd.ExcelWriter('Trial Balance Export.xlsx') as writer:
                # region 0) Variables & workbook Formatting
                exports_check = False  # Variable to check if any data successfully exported

                pref_on = self.main.prefix_on
                pref_accept = self.main.prefix_accepted
                desc_on = self.main.desc_on
                desc_accepted = self.main.desc_accepted

                # Format to export values in two digit numeric format
                workbook = writer.book
                numeric_format = workbook.add_format({'num_format': '0.00'})
                # endregion

                # region 1) Adjusted TB Export
                if self.tb_opt_var_list[0].get() == 1:
                    if desc_on and desc_accepted:
                        tb = self.main.final_tb.copy()
                    elif pref_on and pref_accept:
                        tb = self.main.prefixed_tb.copy()
                    else:
                        self.fp_label.config(text='ERROR: Adj. TB not exported, '
                                                  'neither prefix or desc. corrections performed', fg='#ff684c')
                        return

                    company_field = 'Company New' if 'Company New' in tb.columns else 'Company'
                    code_field = 'Pref. Code' if 'Pref. Code' in tb.columns else 'Code'
                    desc_field = 'Desc. New' if 'Desc. New' in tb.columns else 'Desc.'
                    fields = ['TB Period', company_field, code_field, desc_field, 'Amount']
                    tb = tb[fields]

                    for period in ['Prior TB', 'Opening TB', 'Closing TB']:
                        tb_period = tb[tb['TB Period'] == period]
                        tb_period = tb_period.drop(['TB Period'], axis=1)
                        tb_period.to_excel(writer, sheet_name='Adj ' + period, index=False)

                        worksheet = writer.sheets['Adj ' + period]
                        worksheet.set_column('D:D', None, numeric_format)
                    exports_check = True
                # endregion

                # region 2) Adjusted COA
                if self.coa_opt_var_list[0].get() == 1:
                    coa = self.main.final_coa.copy()

                    code_field = 'Pref. Code' if 'Pref. Code' in tb.columns else 'Code'
                    fsa_field = 'FSA Remap' if 'FSA Remap' in coa else 'FSA'

                    coa.sort_values(by=[fsa_field], na_position='last', inplace=True)
                    fields = [code_field, 'Desc. New', fsa_field]

                    coa = coa[fields]
                    if self.coa_unmap_var.get() == 1:
                        coa.dropna(subset=[fsa_field], inplace=True)

                    coa.to_excel(writer, sheet_name='Adj COA', index=False)
                    exports_check = True
                # endregion

                # region 3) Raw TB Export
                if self.tb_opt_var_list[1].get() == 1:
                    tb = self.main.raw_tb
                    for period in ['Prior TB', 'Opening TB', 'Closing TB']:
                        tb_period = tb[tb['TB Period'] == period]
                        tb_period = tb_period.drop(['TB Period', 'Filename'], axis=1)
                        tb_period.to_excel(writer, sheet_name='Raw ' + period, index=False)

                        worksheet = writer.sheets['Raw ' + period]
                        worksheet.set_column('D:D', None, numeric_format)
                    exports_check = True
                # endregion

                # region 4) Raw COA Export
                if self.coa_opt_var_list[1].get() == 1:
                    coa = self.main.raw_coa
                    coa = coa.drop(['Filename'], axis=1)
                    coa.to_excel(writer, sheet_name='Raw COA', index=False)
                    exports_check = True
                # endregion

                # region 5) Detailed TB Export
                if self.tb_opt_var_list[2].get() == 1:
                    if desc_on and desc_accepted:
                        tb = self.main.final_tb.copy()
                    elif pref_on and pref_accept:
                        tb = self.main.prefixed_tb.copy()
                    else:
                        self.fp_label.config(text='ERROR: Det. TB not exported, '
                                                  'neither prefix or desc. corrections performed', fg='#ff684c')
                        return

                    tb.to_excel(writer, sheet_name='Det. TB', index=False)
                    exports_check = True
                # endregion

                # region 6) Detailed TB Export
                if self.coa_opt_var_list[2].get() == 1:
                    coa = self.main.final_coa
                    coa.to_excel(writer, sheet_name='Det. COA', index=False)
                    exports_check = True
                # endregion

                # region 7) GUI update if no selections made or data exported successfully
                if exports_check:
                    self.fp_label.config(text='Selected Data has been exported to folder', fg='#8ace7e')
                else:
                    self.fp_label.config(text='ERROR: No selections were made', fg='#ff684c')
                # endregion
        except Exception as error:
            self.fp_label.config(text='ERROR: ' + str(error), fg='#ff684c')
    # endregion
