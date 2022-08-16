import tkinter as tk
import pandas as pd
import os
from tkinter import filedialog


class DataExport:
    def __init__(self, master, main):
        self.master = master
        self.main = main
        self.tb = pd.DataFrame()

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
                         'E2-Defer#ff684c Charges',
                         'F-Cash Balances',
                         'F1-Borrowings',
                         'F2-Customer accounts',
                         'F3-Deposits from banks',
                         'G-Accounts Payable',
                         'G1-Long term payables',
                         'H-Other Payables or Accruals',
                         'H1-Defer#ff684c Revenue',
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
                         'H2-Defer#ff684c Capital Grants',
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
        self.master.add(self.top_frame, text='Export Data')
        self.top_frame.columnconfigure(0, weight=1)

        # self.master.tab(4, state="disabled")

        # region GUI
        # ================== 2.0 - Check Data Button ==================
        self.check_frame = tk.Frame(self.top_frame)
        self.check_frame.grid(row=0, column=0, sticky='EW')

        check_data = tk.Button(self.check_frame, text='Review Data for Export:', command=self.check_data, height=2)
        check_data.grid(row=0, column=0, sticky='EW')

        # ================== 2.0 - Final TB Data Format Check ==================

        self.dqi_frame = tk.Frame(self.top_frame)
        self.dqi_frame.grid(row=1, column=0, sticky='EW', ipady=3)

        for x in range(4, 12, 2):
            self.dqi_frame.columnconfigure(x, weight=1)

        # ====== TB DATA ======
        for x, header in zip(range(1, 5), ['PY', 'OP', 'CL', 'Raw TB\nTotals']):
            tk.Label(self.dqi_frame, text=header).grid(row=0, column=x, padx=3, pady=3)

        for y, index in zip(range(1, 7), ['Line Count:', 'Unique\nCompanies:']):
            tk.Label(self.dqi_frame, text=index, height=2).grid(row=y, column=0, sticky='W', padx=3, pady=3)

        # TB Line Entries
        self.py_lines_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.py_lines_entry.grid(row=1, column=1, sticky='NSEW', padx=3, pady=3)
        self.op_lines_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.op_lines_entry.grid(row=1, column=2, sticky='NSEW', padx=3, pady=3)
        self.cl_lines_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.cl_lines_entry.grid(row=1, column=3, sticky='NSEW', padx=3, pady=3)
        self.tot_lines_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.tot_lines_entry.grid(row=1, column=4, sticky='NSEW', padx=3, pady=3)

        # TB Comp. Entries
        self.py_comp_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.py_comp_entry.grid(row=2, column=1, sticky='NSEW', padx=3, pady=3)
        self.op_comp_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.op_comp_entry.grid(row=2, column=2, sticky='NSEW', padx=3, pady=3)
        self.cl_comp_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.cl_comp_entry.grid(row=2, column=3, sticky='NSEW', padx=3, pady=3)
        self.tot_comp_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.tot_comp_entry.grid(row=2, column=4, sticky='NSEW', padx=3, pady=3)

        for x, header in zip(range(5, 10, 2), ['Prefixed', 'Desc.\nChecked', 'Adj. TB\nTotals']):
            print(x)
            tk.Label(self.dqi_frame, text=' > ').grid(row=1, rowspan=2, column=x, sticky='NS')
            tk.Label(self.dqi_frame, text=header).grid(row=0, column=x+1, padx=3, pady=3)

        # TB Adjustments
        self.prefix_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.prefix_entry.grid(row=1, rowspan=2, column=6, sticky='NSEW', padx=3, pady=3)
        self.desc_fix_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.desc_fix_entry.grid(row=1, rowspan=2, column=8, sticky='NSEW', padx=3, pady=3)

        # TB Adjusted totals
        self.tot_adj_lines_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.tot_adj_lines_entry.grid(row=1, column=10, sticky='NSEW', padx=5, pady=3)
        self.tot_adj_comp_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.tot_adj_comp_entry.grid(row=2, column=10, sticky='NSEW', padx=5, pady=3)

        self.tb_spacer = tk.Label(self.dqi_frame, text='V')
        self.tb_spacer.grid(row=3, column=8, sticky='NS')

        # ====== COA DATA ======
        tk.Label(self.dqi_frame, text='Raw\nCOA').grid(row=4, column=4, padx=3, pady=3)
        tk.Label(self.dqi_frame, text='Generate\nNew COA').grid(row=4, column=8, padx=3, pady=3)
        tk.Label(self.dqi_frame, text='Adj.\nCOA').grid(row=4, column=10, padx=3, pady=3)

        for y, index in zip(range(6, 10), ['Line Count:', 'Irregular FSA:', 'Blank FSA:']):
            tk.Label(self.dqi_frame, text=index, height=2).grid(row=y, column=0, sticky='W', padx=3, pady=3)

        # COA Raw Lines/ non standard FSA/ Unmapped
        self.coa_lines_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.coa_lines_entry.grid(row=6, column=4, sticky='NSEW', padx=3, pady=3)
        self.coa_fsa_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.coa_fsa_entry.grid(row=7, column=4, sticky='NSEW', padx=3, pady=3)
        self.coa_unmap_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.coa_unmap_entry.grid(row=8, column=4, sticky='NSEW', padx=3, pady=3)

        tk.Label(self.dqi_frame, text=' > ').grid(row=6, rowspan=3, column=6, sticky='NS', padx=3, pady=3)

        # # COA New COA generated
        self.coa_desc_fix_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.coa_desc_fix_entry.grid(row=6, rowspan=3, column=8, sticky='NSEW', padx=3, pady=3)

        tk.Label(self.dqi_frame, text=' > ').grid(row=6, rowspan=3, column=9, sticky='NS', padx=3, pady=3)

        # COA New Raw Lines/ non-standard FSA/ Unmapped
        self.coa_adj_lines_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.coa_adj_lines_entry.grid(row=6, column=10, sticky='NSEW', padx=5, pady=3)
        self.coa_adj_fsa_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.coa_adj_fsa_entry.grid(row=7, column=10, sticky='NSEW', padx=5, pady=3)
        self.coa_adj_unmap_entry = tk.Entry(self.dqi_frame, width=8, justify='center')
        self.coa_adj_unmap_entry.grid(row=8, column=10, sticky='NSEW', padx=5, pady=3)

        # ================== 3.0 - Export Options ==================

        self.export_opt_frame = tk.Frame(self.top_frame)
        self.export_opt_frame.grid(row=2, column=0, sticky='EW')

        self.tb_label = tk.Label(self.export_opt_frame, text='Trial Balance Exports:')
        self.tb_label.grid(row=0, column=0, sticky='W')

        self.raw_tb_var = tk.IntVar(value=0)
        self.raw_tb_check = tk.Checkbutton(self.export_opt_frame, text='Raw TB',
                                           variable=self.raw_tb_var, state='disabled')
        self.raw_tb_check.grid(row=0, column=1, sticky='W')

        self.adj_tb_var = tk.IntVar(value=0)
        self.adj_tb_check = tk.Checkbutton(self.export_opt_frame, text='Adjusted TB',
                                           variable=self.adj_tb_var, state='disabled')
        self.adj_tb_check.grid(row=0, column=2, sticky='W')

        self.detailed_tb_var = tk.IntVar(value=0)
        self.detailed_tb = tk.Checkbutton(self.export_opt_frame, text='Detailed Meta TB',
                                          variable=self.detailed_tb_var, state='disabled')
        self.detailed_tb.grid(row=0, column=3, sticky='W')

        self.coa_label = tk.Label(self.export_opt_frame, text='Chart of Accounts Exports:')
        self.coa_label.grid(row=1, column=0, sticky='W')

        self.raw_coa_var = tk.IntVar(value=0)
        self.raw_coa_check = tk.Checkbutton(self.export_opt_frame, text='Raw COA',
                                            variable=self.raw_coa_var, state='disabled')
        self.raw_coa_check.grid(row=1, column=1, sticky='W')

        self.adj_coa_var = tk.IntVar(value=0)
        self.adj_coa_check = tk.Checkbutton(self.export_opt_frame, text='Adjusted COA',
                                            variable=self.adj_coa_var, state='disabled')
        self.adj_coa_check.grid(row=1, column=2, sticky='W')

        self.detailed_coa_var = tk.IntVar(value=0)
        self.detailed_coa = tk.Checkbutton(self.export_opt_frame, text='Detailed Meta COA',
                                           variable=self.detailed_coa_var,state='disabled')
        self.detailed_coa.grid(row=1, column=3, sticky='W')

        # ================== 3.0 - Export Path ==================
        self.export_frame = tk.Frame(self.top_frame)
        self.export_frame.grid(row=3, column=0, sticky='EW')
        self.export_frame.columnconfigure(1, weight=1)

        self.fp_button = tk.Button(self.export_frame, text='Open:', command=self.export_path, height=3)
        self.fp_button.grid(row=0, column=0, sticky='EW')
        self.fp_text = tk.StringVar(value='Select Export Directory')
        self.fp_label = tk.Label(self.export_frame, textvariable=self.fp_text)
        self.fp_label.grid(row=0, column=1, sticky='W')
        self.export_button = tk.Button(self.export_frame, text='Export Data', command=self.data_export, height=3)
        self.export_button.grid(row=0, column=2, sticky='EW')
        # endregion

    # region Data check functions
    def reset(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            widget_type = child.winfo_class()
            if widget_type == 'Entry':
                child.delete(0, tk.END)
            else:
                self.reset(child)

    def check_data(self):
        # 1) Clear all TB Period widgets
        self.reset(self.dqi_frame)

        # ========= RAW TB DATA CHECKS =========

        # 1) Get Raw TB & Widgets to insert
        raw_tb = self.main.raw_tb
        line_widgets = [[self.py_lines_entry, self.py_comp_entry],
                        [self.op_lines_entry, self.op_comp_entry],
                        [self.cl_lines_entry, self.cl_comp_entry]]
        line_widgets: list

        if len(raw_tb) != 0:
            # 2) Populate entries split by period
            for period, widget in zip(['Prior TB', 'Opening TB', 'Closing TB'], line_widgets):
                # 2.1) Populate lines for each period
                lines = raw_tb[raw_tb['TB Period'] == period]
                widget[0].insert(0, str(len(lines)))

                # 2.2) Populate companies for each period
                companies = lines['Company'].unique().tolist()
                widget[1].insert(0, str(len(companies)))

            # 3) Update Raw data widgets
            self.tot_lines_entry.insert(0, str(len(raw_tb)))
            self.tot_comp_entry.insert(0, str(len(set(raw_tb['Company'].unique().tolist()))))
            self.raw_tb_check.config(state='normal')
        else:
            for widget in line_widgets:
                widget[0].insert(0, 'NULL')
                widget[1].insert(0, 'NULL')
            self.tot_lines_entry.insert(0, 'NULL')
            self.tot_comp_entry.insert(0, 'NULL')
            self.raw_tb_check.config(state='disabled')

        # ========= RAW COA DATA CHECKS =========
        raw_coa = self.main.raw_coa

        if len(raw_coa) != 0:
            self.coa_lines_entry.insert(0, str(len(raw_coa)))
            self.coa_unmap_entry.insert(0, str(raw_coa['FSA'].isnull().sum()))
            self.coa_fsa_entry.insert(0, str(len(raw_coa[~raw_coa['FSA'].isin(self.fsa_list)])))
            self.raw_coa_check.config(state='normal')
        else:
            self.coa_lines_entry.insert(0, 'NULL')
            self.coa_unmap_entry.insert(0, 'NULL')
            self.coa_fsa_entry.insert(0, 'NULL')
            self.raw_coa_check.config(state='disabled')

        # ========= RAW TB & COA SELECTION CHECKS =========

        # 1) Check Prefix Mappings, update TB & COA entries
        pref_on = self.main.prefix_on
        pref_accept = self.main.prefix_accepted
        pref_colour = '#8ace7e' if not pref_on else '#8ace7e' if pref_accept else '#ff684c'
        pref_text = 'Not Selected' if not pref_on else 'Complete' if pref_accept else 'Error'
        self.prefix_entry.insert(0, pref_text)
        self.prefix_entry.config(bg=pref_colour)

        # 2) Check Description Mappings, update TB entry
        desc_on = self.main.desc_on
        desc_accepted = self.main.desc_accepted
        desc_colour = '#ffda66' if not desc_on else '#8ace7e' if desc_accepted else '#ff684c'
        desc_text = 'Not Checked' if not desc_on else 'Complete' if desc_accepted else 'Error'
        self.desc_fix_entry.insert(0, desc_text)
        self.desc_fix_entry.config(bg=desc_colour)

        # 3) Check if COA was regenerated, update COA entries
        coa_accepted = self.main.coa_accepted
        print('COA ACCEPTED IS: ' + str(coa_accepted))
        coa_colour = '#ffda66' if not desc_on else '#8ace7e' if coa_accepted else '#ff684c'
        coa_text = 'Desc. Not Checked' if not desc_on else 'Complete' if coa_accepted else 'Error'
        self.coa_desc_fix_entry.insert(0, coa_text)
        self.coa_desc_fix_entry.config(bg=coa_colour)

        # ========= FINAL TB DATA CHECKS =========

        # 1) Assign TB based on selections
        if desc_on and desc_accepted:
            tb = self.main.final_tb.copy()
        elif pref_on and pref_accept:
            tb = self.main.prefixed_tb.copy()
        else:
            tb = self.main.raw_tb.copy()

        # 2) Update GUI Mappings
        if len(tb) != 0:
            self.tot_adj_lines_entry.insert(0, str(len(tb)))
            comp_field = 'Company New' if pref_on and pref_accept else 'Company'
            self.tot_adj_comp_entry.insert(0, str(len(tb[comp_field].unique().tolist())))
            self.adj_tb_check.config(state='normal')
            self.detailed_tb.config(state='normal')
        else:
            self.tot_adj_lines_entry.insert(0, 'NULL')
            self.tot_adj_comp_entry.insert(0, 'NULL')
            self.adj_tb_check.config(state='disabled')
            self.detailed_tb.config(state='disabled')

        # ========= FINAL COA DATA CHECKS =========

        # 1) Assign COA based on selections
        if desc_on and coa_accepted:
            coa = self.main.final_coa.copy()
            print('EXPORT COA')
            print(coa)

            if len(coa) != 0:
                self.coa_adj_lines_entry.insert(0, str(len(coa)))
                self.coa_adj_unmap_entry.insert(0, str(coa['FSA New'].isnull().sum()))
                coa.dropna(subset=['FSA New'], inplace=True)
                self.coa_adj_fsa_entry.insert(0, str(len(coa[~coa['FSA New'].isin(self.fsa_list)])))
                self.adj_coa_check.config(state='normal')
                self.detailed_coa.config(state='normal')
            else:
                self.coa_adj_lines_entry.insert(0, 'NULL')
                self.coa_adj_unmap_entry.insert(0, 'NULL')
                self.coa_adj_fsa_entry.insert(0, 'NULL')
                self.adj_coa_check.config(state='disabled')
                self.detailed_coa.config(state='disabled')
        else:
            self.coa_adj_lines_entry.insert(0, 'COA not generated.')
            self.coa_adj_unmap_entry.insert(0, 'COA not generated.')
            self.coa_adj_fsa_entry.insert(0, 'COA not generated.')
            self.adj_coa_check.config(state='disabled')
            self.detailed_coa.config(state='disabled')
    # endregion

    def export_path(self):
        try:
            # 1) Select filepath and update tkinter text with path
            fp = filedialog.askdirectory(initialdir='/', title='Select a directory')

            # 2) Sets GUI label to selected filepath, exits function if not selected
            if len(fp) != 0:
                self.fp_text.set(str(fp))
                self.export_button['state'] = 'normal'
                os.chdir(fp)
            else:
                self.fp_text.set('ERROR: No Filepath was selected')
                self.export_button['state'] = 'disable'
                return
        # Filepath error handling exception
        except os.error:
            self.fp_text.set('ERROR: Invalid Directory')
            self.export_button['state'] = 'disable'

    def data_export(self):
        print(os.listdir())

        with pd.ExcelWriter('Trial Balance Export.xlsx') as writer:
            exports_check = False

            # RAW TB DATA EXPORT
            if self.raw_tb_var.get() == 1:
                tb = self.main.raw_tb

                # Divide data by period
                py = tb[tb['TB Period'] == 'Prior TB']
                py = py.drop(['TB Period', 'Filename'], axis=1)
                py.to_excel(writer, sheet_name='RAW PY', index=False)
                op = tb[tb['TB Period'] == 'Opening TB']
                op = op.drop(['TB Period', 'Filename'], axis=1)
                op.to_excel(writer, sheet_name='RAW OP', index=False)
                cl = tb[tb['TB Period'] == 'Closing TB']
                cl = cl.drop(['TB Period', 'Filename'], axis=1)
                cl.to_excel(writer, sheet_name='RAW CL', index=False)

                exports_check = True

            # RAW COA DATA EXPORT
            if self.raw_coa_var.get() == 1:
                coa = self.main.raw_coa
                coa = coa.drop(['Filename'], axis=1)
                coa.to_excel(writer, sheet_name='RAW COA', index=False)

                exports_check = True

            # ADJUSTED TB DATA EXPORT
            if self.adj_tb_var.get() == 1:
                pref_on = self.main.prefix_on
                pref_accept = self.main.prefix_accepted
                desc_on = self.main.desc_on
                desc_accepted = self.main.desc_accepted

                if desc_on and desc_accepted:
                    tb = self.main.final_tb.copy()
                elif pref_on and pref_accept:
                    tb = self.main.prefixed_tb.copy()
                else:
                    print('ERROR: Neither Descriptions or Prefixes were performed Correctly')

                company_field = 'Company New' if 'Company New' in tb.columns else 'Company'
                code_field = 'Pref. Code' if 'Pref. Code' in tb.columns else 'Code'
                desc_field = 'Desc. New' if 'Desc. New' in tb.columns else 'Desc.'
                fields = ['TB Period', company_field, code_field, desc_field, 'Amount']
                print(fields)

                print('Final TB DATA IS:')
                tb = tb[fields]
                print(tb)

                # Divide data by period
                py = tb[tb['TB Period'] == 'Prior TB']
                py = py.drop(['TB Period'], axis=1)
                py.to_excel(writer, sheet_name='ADJ PY', index=False)

                op = tb[tb['TB Period'] == 'Opening TB']
                op = op.drop(['TB Period'], axis=1)
                op.to_excel(writer, sheet_name='ADJ OP', index=False)

                cl = tb[tb['TB Period'] == 'Closing TB']
                cl = cl.drop(['TB Period'], axis=1)
                cl.to_excel(writer, sheet_name='ADJ CL', index=False)

                exports_check = True

            # DETAILED TB DATA EXPORT
            if self.detailed_tb_var.get() == 1:
                pref_on = self.main.prefix_on
                pref_accept = self.main.prefix_accepted
                desc_on = self.main.desc_on
                desc_accepted = self.main.desc_accepted

                if desc_on and desc_accepted:
                    tb = self.main.final_tb.copy()
                elif pref_on and pref_accept:
                    tb = self.main.prefixed_tb.copy()
                else:
                    print('ERROR: Neither Descriptions or Prefixes were performed Correctly')

                tb.to_excel(writer, sheet_name='DETAILED TB', index=False)

                exports_check = True

            # ADJUSTED COA DATA EXPORT
            if self.adj_coa_var.get() == 1:
                coa = self.main.final_coa

                code_field = 'Pref. Code' if 'Pref. Code' in tb.columns else 'Code'
                fields = [code_field, 'Desc. New', 'FSA New']

                coa = coa[fields]

                print('Final COA DATA IS:')
                print(coa)

                coa.to_excel(writer, sheet_name='ADJ COA', index=False)

                exports_check = True

            # DETAILED COA DATA EXPORT
            if self.detailed_coa_var.get() == 1:
                coa = self.main.final_coa

                print('DETAILED COA DATA IS:')
                print(coa)

                coa.to_excel(writer, sheet_name='DETAILED COA', index=False)

                exports_check = True

            if exports_check:
                self.fp_text.set('Selected Data has been exported to folder')
                self.fp_label.config(fg='#8ace7e')
            else:
                self.fp_text.set('ERROR: No selections were made')
                self.fp_label.config(fg='#ff684c')


