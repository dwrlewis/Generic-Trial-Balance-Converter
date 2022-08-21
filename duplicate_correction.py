import tkinter as tk
from tkinter import ttk
import pandas as pd


class DuplicateCorrection:
    def __init__(self, master, main):
        self.master = master
        self.main = main

        self.pref_on = self.main.prefix_on  # Checks if prefixes were selected on in previous tab
        self.pref_accept = self.main.prefix_accepted  # Checks if prefix mappings were accepted in previous tab

        self.imported_tb = pd.DataFrame()  # Imported from either raw_tb or prefixed_tb
        self.desc_options = pd.DataFrame()  # Dataframe of codes with multiple descriptions (TB Period, Code, Desc.)

        self.dupe_limit = False  # Flagged True if number of inconsistent codes exceeds GUI limits

        self.desc_mappings = pd.DataFrame()  # Filtered Mapping dataframe with selected remapping

        # region Tkinter GUI
        # ================== 0.0 - Top Frame ==================
        self.top_frame = tk.Frame(master)
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.master.add(self.top_frame, text='Description Settings')
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(1, weight=1)

        # self.master.tab(2, state="disabled")

        # ================== 1.0 - Description Mapping On/Off ==================
        # Prefix on/off Frame
        self.on_off_frame = tk.Frame(self.top_frame)
        self.on_off_frame.grid(row=0, column=0, sticky='EW')

        self.on_off_label = tk.Label(self.on_off_frame, text='Correct inconsistent account descriptions:')
        self.on_off_label.grid(row=0, column=0, columnspan=2, sticky='EW')

        for x in range(2):
            self.on_off_frame.columnconfigure(x, weight=1)

        self.desc_remap_var = tk.IntVar(value=0)
        self.on_button = tk.Radiobutton(self.on_off_frame, text='Yes', variable=self.desc_remap_var, value=1,
                                        command=self.enable_canvas)
        self.on_button.grid(row=1, column=0)
        self.off_button = tk.Radiobutton(self.on_off_frame, text='No', variable=self.desc_remap_var, value=0,
                                         command=self.disable_canvas)
        self.off_button.grid(row=1, column=1)

        self.warning_frame = tk.Frame(self.top_frame)
        self.warning_frame.grid(row=0, column=1, sticky='NSEW')
        self.warn_label = tk.Label(self.warning_frame,
                                   text='Descriptions will not be adjusted. New COA cannot be generated without\n'
                                        'checking descriptions first, unadjusted raw COA will be exported instead.',
                                   fg='#8ace7e')
        self.warn_label.grid(row=0, column=0, sticky='W')

        # ================== 2.0 - Options Frame ==================
        self.options_frame = tk.Frame(self.top_frame)
        self.options_frame.grid(row=1, column=0, sticky='NSEW')
        self.options_frame.columnconfigure(0, weight=1)

        # ================== 2.1 - Join Mappings ==================
        self.join_frame = tk.Frame(self.options_frame)
        self.join_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        self.join_frame.columnconfigure(0, weight=1)

        self.join_frame_label = tk.Label(self.join_frame, text='Check Descriptions:')
        self.join_frame_label.grid(row=0, column=0, sticky='W')

        # Trim blanks checkbox
        self.trim = tk.IntVar()
        self.trim.set(1)
        self.trim_checkbox = tk.Checkbutton(self.join_frame, text='Trim leading & trailing spaces',
                                            variable=self.trim)
        self.trim_checkbox.grid(row=1, column=0, sticky='W')

        # Map to upper/lower cases
        self.case_frame = tk.Frame(self.join_frame)
        self.case_frame.grid(row=2, column=0, sticky='EW')

        self.case_label = tk.Label(self.case_frame, text='Adjust description casings:')
        self.case_label.grid(row=0, column=0, columnspan=3, sticky='W')

        # Radio button Var
        self.case_var = tk.IntVar()
        self.case_var.set(0)
        # No change - Radio Button
        self.case_upper = tk.Radiobutton(self.case_frame, text='No Change', variable=self.case_var, value=0)
        self.case_upper.grid(row=1, column=0)
        # Lower - Radio Button
        self.case_lower = tk.Radiobutton(self.case_frame, text='Lower', variable=self.case_var, value=1)
        self.case_lower.grid(row=1, column=1)
        # Upper - Radio Button
        self.case_lower = tk.Radiobutton(self.case_frame, text='Upper', variable=self.case_var, value=2)
        self.case_lower.grid(row=1, column=2)

        # Check duplicates button
        self.join_button = tk.Button(self.join_frame, text='Check Descriptions:',
                                     command=self.flag_duplicates
                                     )
        self.join_button.grid(row=3, column=0, sticky='NSEW')

        # ================== 2.2 - Auto Mappings ==================
        self.auto_map_frame = tk.Frame(self.options_frame)
        self.auto_map_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=5)
        self.auto_map_frame.columnconfigure(0, weight=1)

        self.auto_map_label = tk.Label(self.auto_map_frame, text='Auto Map Descriptions:')
        self.auto_map_label.grid(row=0, column=0, sticky='W')

        # Priority mapping Option menu
        self.priority = tk.StringVar()
        self.auto_map_list = ['CL > OP > PY',
                              'CL > PY > OP',
                              'OP > CL > PY',
                              'OP > PY > CL',
                              'PY > OP > CL',
                              'PY > CL > OP'
                              ]
        self.auto_map_options = ttk.Combobox(self.auto_map_frame, textvariable=self.priority, values=self.auto_map_list)
        self.auto_map_options.current(0)
        self.auto_map_options.grid(row=1, column=0, columnspan=2, sticky='NSEW')

        # Priority mapping description (default longest string)
        # Map to upper/lower cases
        self.str_len_frame = tk.Label(self.auto_map_frame, text='String prioritization rule:')
        self.str_len_frame.grid(row=2, column=0, columnspan=2, sticky='W')
        # Radio button Var
        self.str_len_var = tk.IntVar()
        self.str_len_var.set(0)
        # No change - Radio Button
        self.str_len_upper = tk.Radiobutton(self.auto_map_frame, text='Longest string',
                                            variable=self.str_len_var, value=0)
        self.str_len_upper.grid(row=3, column=0)
        # Lower - Radio Button
        self.str_len_lower = tk.Radiobutton(self.auto_map_frame, text='First instance',
                                            variable=self.str_len_var, value=1)
        self.str_len_lower.grid(row=3, column=1)

        # Check duplicates button
        self.auto_map_button = tk.Button(self.auto_map_frame, text='Auto-Map Descriptions',
                                         command=self.auto_map_desc
                                         )
        self.auto_map_button.grid(row=4, column=0, columnspan=2, sticky='NSEW')

        # ================== 4.0 - Main Canvas Frame ==================
        self.can_frame = tk.LabelFrame(self.top_frame)
        self.can_frame.grid(row=1, column=1, sticky='NSEW')
        for x in range(2):
            self.can_frame.columnconfigure(x, weight=1)
        self.can_frame.rowconfigure(1, weight=1)
        # ================== 4.1 - Header Canvas Frame ==================
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

        # ================== 4.2 - Data Canvas Frame ==================
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

        # ================== 3.0 - Check Button ==================
        self.replace_desc_frame = tk.Label(self.top_frame)
        self.replace_desc_frame.grid(row=2, column=0, sticky='NSEW')
        self.replace_desc_frame.columnconfigure(0, weight=1)

        # Check mappings button
        self.replace_desc_button = tk.Button(self.replace_desc_frame, text='Check & Save Mappings:', height=3,
                                             command=self.map_descriptions
                                             )
        self.replace_desc_button.grid(row=0, column=0, sticky='EW')

        self.replace_desc_frame_2 = tk.Frame(self.top_frame)
        self.replace_desc_frame_2.grid(row=2, column=1, sticky='NSEW')
        self.replace_desc_frame_2.columnconfigure(0, weight=1)
        self.replace_desc_frame_2.rowconfigure(0, weight=1)

        self.replace_desc_label = tk.Label(self.replace_desc_frame_2, text='', anchor='w')
        self.replace_desc_label.grid(row=0, column=0, sticky='NSW')

        # Disable elements initially
        self.disable_children(self.options_frame)
        # endregion

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
    def enable_canvas(self):
        self.main.desc_on = True
        self.warn_label.config(text='Please adjust formatting options and Check Descriptions')

        self.enable_children(self.join_frame)

    def enable_children(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            widget_type = child.winfo_class()
            if widget_type not in ('Frame', 'Labelframe', 'Scrollbar'):
                child.configure(state='normal')
            else:
                # 2) Repeats loops with sub_children of widget
                self.enable_children(child)

    def disable_canvas(self):
        self.main.desc_on = False
        # Resets canvas (recheck for memory leaks)
        self.data_can.delete()
        self.data_can.delete(self.data_can_window)
        # New Canvas
        self.data_can = tk.Canvas(self.can_frame)
        self.data_can.grid(row=1, column=0, columnspan=5, sticky='NSEW')
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

        self.warn_label.config(text='Descriptions will not be adjusted. New COA cannot be generated without\n'
                                    'checking descriptions first, unadjusted raw COA will be exported instead.',
                               fg='#8ace7e')

        self.disable_children(self.options_frame)

        self.main.colour(self.can_frame)

    def disable_children(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            widget_type = child.winfo_class()
            if widget_type not in ('Frame', 'Labelframe', 'Canvas', 'Scrollbar'):
                child.configure(state='disable')
            else:
                # 2) Repeats loops with sub_children of widget
                self.disable_children(child)

    # endregion

    # Generate list of descriptions
    def flag_duplicates(self):
        # 1) Get variables for if prefixes were set on, and if mappings were accepted
        pref_on = self.main.prefix_on
        pref_accept = self.main.prefix_accepted
        print(pref_on)

        # 2) Assign raw tb or prefixed tb to local variable as well as desc_incon for filtering
        # REARRANGE GUI UPDATE TO LATER, THIS IS #ff684cUNDANT HERE
        if pref_on and pref_accept:
            self.imported_tb = self.main.prefixed_tb.copy()
        elif pref_on and not pref_accept:
            self.warn_label.config(text='Prefixed Codes selected but not mapped/saved correctly.'
                                        '\nPlease review Prefix Settings tab.',
                                   fg='#ff684c')
            return
        else:
            self.imported_tb = self.main.raw_tb.copy()
            self.warn_label.config(text='Raw TB Code descriptions checked for inconsistencies.',
                                   fg='#8ace7e')

        # print('========= IMPORTED TB ==========')
        # Create another dataframe copy for editing down to codes with multiple descriptions
        multiple_desc = self.imported_tb.copy()
        # Converts NaN's to nan's, needed for filtering by uniques
        multiple_desc['Desc.'] = multiple_desc['Desc.'].astype(str)

        # 3) Trim descriptions if selected
        if self.trim.get() == 1:
            multiple_desc['Desc.'] = multiple_desc['Desc.'].str.strip()
        # 4) Adjust descriptions to upper or lower case if selected
        if self.case_var.get() == 1:
            multiple_desc['Desc.'] = multiple_desc['Desc.'].str.lower()
        elif self.case_var.get() == 2:
            multiple_desc['Desc.'] = multiple_desc['Desc.'].str.upper()

        # 5) Prefix selection is used to determine which field codes are drawn from
        code_field = 'Pref. Code' if self.main.prefix_on else 'Code'

        # 5) Filter for account codes with more than one description
        multiple_desc = multiple_desc.groupby(code_field).filter(lambda tb: tb['Desc.'].nunique() > 1)

        # 6) Create unique field to filter out multiple instances of flagged code & descriptions & drop columns
        multiple_desc['Uniques'] = multiple_desc[code_field] + multiple_desc['Desc.']
        multiple_desc.drop_duplicates(subset=['Uniques'], inplace=True)
        multiple_desc.sort_values(code_field, inplace=True)

        drop_fields = ['Filename', 'Company', 'Code', 'Amount', 'Company New', 'Uniques'] if self.main.prefix_on else \
            ['Filename', 'Company', 'Amount', 'Uniques']
        multiple_desc.drop(columns=drop_fields, axis=1, inplace=True)

        print('====== MULTI DESC. INSTANCES ======')
        self.desc_options = multiple_desc
        print(self.desc_options)

        # 7) Reset GUI canvas
        for widgets in self.data_can_sub_frame.winfo_children():
            widgets.destroy()

        # 8) Update GUI depending on volume of duplicates found
        if multiple_desc.empty:
            self.dupe_limit = False
            self.main.desc_accepted = True
            self.imported_tb['Desc. New'] = self.imported_tb['Desc.']
            print(self.imported_tb)
            self.main.final_tb = self.imported_tb
            self.warn_label.config(text='No inconsistent descriptions found. Proceed to COA Mapping Tab.',
                                   fg='#8ace7e')

            # Disable GUI
            self.disable_children(self.auto_map_frame)
            self.disable_children(self.can_frame)
            self.disable_children(self.replace_desc_frame)
            self.disable_children(self.replace_desc_frame_2)

            # Auto save current mappings?

        elif int(multiple_desc[[code_field]].nunique()) > 300:
            self.dupe_limit = True
            self.warn_label.config(text=str(int(multiple_desc[[code_field]].nunique())) +
                                   ' inconsistent descriptions found, exceeds display limits.'
                                   '\nPlease refer to Auto Map to correct duplicates.',
                                   fg='#ffda66')

            # enable gui due to adjustments needed?
            self.enable_children(self.auto_map_frame)
            self.enable_children(self.can_frame)
            self.enable_children(self.replace_desc_frame)
            self.enable_children(self.replace_desc_frame_2)

        else:
            self.dupe_limit = False
            self.warn_label.config(text=str(int(multiple_desc[[code_field]].nunique())) +
                                   ' inconsistent descriptions found, please select mappings.',
                                   fg='#ffda66')

            # enable gui due to adjustments needed?
            self.enable_children(self.auto_map_frame)
            self.enable_children(self.can_frame)
            self.enable_children(self.replace_desc_frame)
            self.enable_children(self.replace_desc_frame_2)

            # 8) Convert duplicates dataframe into list of lists, first element code, then list of option
            dupes_list = multiple_desc.groupby(code_field)['Desc.'].apply(lambda desc: [desc.name, *desc]).tolist()

            for x in dupes_list:
                y = dupes_list.index(x)

                code = tk.Entry(self.data_can_sub_frame)
                code.insert(0, x[0])
                code.grid(row=y, column=0, sticky='EW')
                code.config(state='readonly')

                desc_options = x[1:]
                multiple_desc = ttk.Combobox(self.data_can_sub_frame, values=desc_options)
                multiple_desc.grid(row=y, column=1, sticky='EW')

    def auto_map_desc(self):
        self.desc_mappings = pd.DataFrame()  # Reset Mapping dataframe
        # Get GUI selection and use dictionary to get priority order of tabs
        priority_dictionary = {'CL > OP > PY': ['Closing TB', 'Opening TB', 'Prior TB'],
                               'CL > PY > OP': ['Closing TB', 'Prior TB', 'Opening TB'],
                               'OP > CL > PY': ['Opening TB', 'Closing TB', 'Prior TB'],
                               'OP > PY > CL': ['Opening TB', 'Prior TB', 'Closing TB'],
                               'PY > OP > CL': ['Prior TB', 'Opening TB', 'Closing TB'],
                               'PY > CL > OP': ['Prior TB', 'Closing TB', 'Opening TB']
                               }
        priority_check = priority_dictionary[self.priority.get()]

        code_field = 'Pref. Code' if self.main.prefix_on else 'Code'

        # If lines exceed display limited
        if not self.dupe_limit:
            # Gets widgets in two column list of lists
            canvas_widgets = self.data_can_sub_frame.winfo_children()
            widget_array = [canvas_widgets[x:x + 2] for x in range(0, len(canvas_widgets), 2)]

            for row in widget_array:
                row: list
                code = row[0].get()
                mappings = self.desc_options[self.desc_options[code_field] == code]

                for x in range(3):
                    if priority_check[x] in mappings['TB Period'].values:
                        # Filter to prioritised period
                        priority_map = mappings[mappings['TB Period'] == priority_check[x]]
                        # Convert to list
                        priority_map = priority_map['Desc.'].astype(str).tolist()
                        # print(priority_map)

                        # Filter for longest string remaining or first instance listed
                        if self.str_len_var.get() == 1:
                            desc_mapping = priority_map[0]
                        else:
                            desc_mapping = max(priority_map, key=len)

                        # print(desc_mapping)
                        row[1].set(desc_mapping)
                        break

        else:
            # 1) Get copy of imported TB data, either raw or prefixed
            tb = self.desc_options

            # 2) Generate period priority field from 1 to 3, 4 as null placement
            tb['Filter Column'] = 4
            tb.loc[tb['TB Period'] == priority_check[0], 'Filter Column'] = 1
            tb.loc[tb['TB Period'] == priority_check[1], 'Filter Column'] = 2
            tb.loc[tb['TB Period'] == priority_check[2], 'Filter Column'] = 3

            # 3) Generate description length field
            tb['String len'] = tb['Desc.'].str.len()

            # 4) Sort based on selections for longest string or first instance
            if self.str_len_var.get() == 1:
                tb = tb.sort_values(by=['Filter Column', code_field, 'String len', 'Desc.'],
                                    ascending=[True, True, False, True], axis=0)
            else:
                tb = tb.sort_values(by=['Filter Column', code_field, 'Desc.'],
                                    ascending=[True, True, True], axis=0)

            # 5) Drop duplicates and useless fields to get descriptions mapping dataframe
            tb.drop_duplicates(subset=[code_field], keep='first', inplace=True)
            tb.drop(columns=['TB Period', 'Filter Column', 'String len'],
                    axis=1, inplace=True)

            self.desc_mappings = tb

            print('======= DESC. MAPPING - NO GUI DISPLAY =========')
            print(self.desc_mappings)
            print('Length of desc. Mapping: ' + str(len(tb)))
            print('Unique Codes in desc. Mapping: ' + str(tb[code_field].nunique()))

    def map_descriptions(self):
        self.main.final_tb = pd.DataFrame()
        # print('map new descriptions')
        error_flag = False
        code_field = 'Pref. Code' if self.main.prefix_on else 'Code'

        if not self.dupe_limit:
            # Gets widgets in two column list of lists, Check if any descriptions have been left unmapped
            canvas_widgets = self.data_can_sub_frame.winfo_children()
            widget_array = [canvas_widgets[x:x + 2] for x in range(0, len(canvas_widgets), 2)]
            widget_array: list
            for row in widget_array:
                if len(row[1].get().strip()) == 0:
                    error_flag = True
                    row[0].config(readonlybackground='#ff684c')
                else:
                    row[0].config(readonlybackground='#8ace7e')

            if not error_flag:
                join = [[row[0].get(), row[1].get()] for row in widget_array]
                join_df = pd.DataFrame(join, columns=[code_field, 'Desc.'])
                tb_new_desc = pd.merge(self.imported_tb, join_df, on=code_field, how='left', suffixes=('', ' New'))

                # tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'], inplace=True) # ORIGINAL SCRIPT PRE 19/06/22

                # Adjusted to Account for Casing selections # ADJUSTMENT MADE 19/06/22
                print('ERROR CHECKING DESCRIPTIONS')
                print(self.case_var.get())

                if self.case_var.get() == 1:
                    tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.lower(), inplace=True)
                    print('DESCS ON FINAL TB CONVERTED TO LOWER')
                elif self.case_var.get() == 2:
                    tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.upper(), inplace=True)
                    print('DESCS ON FINAL TB CONVERTED TO UPPER')
                else:
                    tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'], inplace=True)

                self.main.final_tb = tb_new_desc.copy()
            else:
                self.replace_desc_label.config(
                    text='Descriptions mappings have not beem selected, highlighted in #ff684c.')
                self.master.tab(3, state="disabled")
                return

        else:
            tb_new_desc = pd.merge(self.imported_tb, self.desc_mappings, on=code_field, how='left',
                                   suffixes=('', ' New'))

            # tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'], inplace=True) # ORIGINAL SCRIPT PRE 19/06/22

            print('ERROR CHECKING DESCRIPTIONS')
            print(self.case_var.get())

            # Adjusted to Account for Casing selections # ADJUSTMENT MADE 19/06/22
            if self.case_var.get() == 1:
                tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.lower(), inplace=True)
                print('DESCS ON FINAL TB CONVERTED TO LOWER')
            elif self.case_var.get() == 2:
                tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.upper(), inplace=True)
                print('DESCS ON FINAL TB CONVERTED TO UPPER')
            else:
                tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'], inplace=True)

            self.main.final_tb = tb_new_desc.copy()

        print('====== FINAL TB - DUPLICATE CHECKED ======')
        print(self.main.final_tb)

        desc_check = self.main.final_tb.groupby(code_field).filter(lambda x: x['Desc. New'].nunique() > 1)
        print(desc_check)

        if len(desc_check) == 0:
            self.main.desc_accepted = True
            self.replace_desc_label.config(text='Trial balance has been updated with consistent descriptions',
                                           fg='#8ace7e')
            self.master.tab(3, state="normal")
            print('NO DUPLICATES')
        else:
            self.main.desc_accepted = False
            self.replace_desc_label.config(text='ERROR: Internal process error, duplicates present after filtering.',
                                           fg='#ff684c')
            self.master.tab(3, state="disabled")
            print('DUPLICATES PRESENT')
