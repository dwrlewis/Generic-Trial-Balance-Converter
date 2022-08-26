import tkinter as tk
from tkinter import ttk
import pandas as pd


class DuplicateCorrection:
    def __init__(self, master, main):
        self.master = master
        self.main = main

        # region variables
        self.pref_on = self.main.prefix_on  # Checks if prefixes were selected on in previous tab
        self.pref_accept = self.main.prefix_accepted  # Checks if prefix mappings were accepted in previous tab

        self.imported_tb = pd.DataFrame()  # Imported from either raw_tb or prefixed_tb
        self.desc_options = pd.DataFrame()  # Dataframe of codes with multiple descriptions (TB Period, Code, Desc.)

        self.dupe_limit = False  # Flagged True if number of inconsistent codes exceeds GUI limits

        self.desc_mappings = pd.DataFrame()  # Filtered Mapping dataframe with selected remapping
        # endregion

        # region ================== 0.0 - Top Frame ==================
        self.top_frame = tk.Frame(master)
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        self.master.add(self.top_frame, text='Description Settings')
        self.master.tab(2, state='disabled')
        # endregion

        # region ================== 1.0 - Description Mapping On/Off ==================
        self.on_off_frame = tk.Frame(self.top_frame)
        self.on_off_frame.grid(row=0, column=0, sticky='EW')
        for x in range(2):
            self.on_off_frame.columnconfigure(x, weight=1)
        # Desc. On/Off Label
        self.on_off_label = tk.Label(self.on_off_frame, text='Correct inconsistent account descriptions:')
        self.on_off_label.grid(row=0, column=0, columnspan=2, sticky='EW')
        # Desc. On/Off Radio-Buttons
        self.desc_var = tk.IntVar(value=0)
        self.on_button = tk.Radiobutton(self.on_off_frame, text='Yes', variable=self.desc_var, value=1,
                                        command=self.enable_canvas)
        self.on_button.grid(row=1, column=0)
        self.off_button = tk.Radiobutton(self.on_off_frame, text='No', variable=self.desc_var, value=0,
                                         command=self.disable_canvas)
        self.off_button.grid(row=1, column=1)
        # Desc. Warning Frame & Label
        self.on_off_warn_frame = tk.Frame(self.top_frame)
        self.on_off_warn_frame.grid(row=0, column=1, sticky='NSEW')
        self.on_off_warn_label = tk.Label(self.on_off_warn_frame, fg='#8ace7e',
                                          text='Descriptions will not be adjusted. COA cannot be generated without\n'
                                               ' checking descriptions, raw COA will be exported instead.')
        self.on_off_warn_label.grid(row=0, column=0, sticky='W')
        # endregion

        # region ================== 2.0 - Options Frame ==================
        self.options_frame = tk.Frame(self.top_frame)
        self.options_frame.grid(row=1, column=0, sticky='NSEW')
        self.options_frame.columnconfigure(0, weight=1)

        # region ================== 2.1 - Join Mappings ==================
        self.join_frame = tk.Frame(self.options_frame)
        self.join_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        for x in range(3):
            self.join_frame.columnconfigure(x, weight=1)
        # Header Label - 'Check Descriptions'
        self.join_label_header = tk.Label(self.join_frame, text='Check Descriptions:')
        self.join_label_header.grid(row=0, column=0, columnspan=3, sticky='W')
        # Trim blanks checkbox
        self.trim_var = tk.IntVar()
        self.trim_var.set(1)
        self.join_check = tk.Checkbutton(self.join_frame, text='Trim leading & trailing spaces', variable=self.trim_var)
        self.join_check.grid(row=1, column=0, columnspan=3, sticky='W')
        # Header Label - 'Adjust description casings'
        self.case_label = tk.Label(self.join_frame, text='Adjust Description Casings:')
        self.case_label.grid(row=2, column=0, columnspan=3, sticky='W')
        # Case Changing - Radio Button
        self.case_var = tk.IntVar(value=0)
        self.join_upper = tk.Radiobutton(self.join_frame, text='No Change', variable=self.case_var, value=0)
        self.join_upper.grid(row=3, column=0)
        self.join_lower = tk.Radiobutton(self.join_frame, text='Lower', variable=self.case_var, value=1)
        self.join_lower.grid(row=3, column=1)
        self.join_lower = tk.Radiobutton(self.join_frame, text='Upper', variable=self.case_var, value=2)
        self.join_lower.grid(row=3, column=2)
        # Check duplicates button
        self.join_button = tk.Button(self.join_frame, text='Check Descriptions:', command=self.flag_duplicates)
        self.join_button.grid(row=4, column=0, columnspan=3, sticky='NSEW')
        # endregion

        # region ================== 2.2 - Auto Mappings ==================
        # Auto-Mapping Frame & Label
        self.map_frame = tk.Frame(self.options_frame)
        self.map_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=5)
        self.map_frame.columnconfigure(0, weight=1)
        self.map_label = tk.Label(self.map_frame, text='Auto Map Descriptions:')
        self.map_label.grid(row=0, column=0, columnspan=2, sticky='W')
        # Auto-Mapping Tab Priority
        self.priority = tk.StringVar()
        self.map_list = ['CL > OP > PY',
                         'CL > PY > OP',
                         'OP > CL > PY',
                         'OP > PY > CL',
                         'PY > OP > CL',
                         'PY > CL > OP'
                         ]
        self.map_options = ttk.Combobox(self.map_frame, textvariable=self.priority, values=self.map_list)
        self.map_options.current(0)
        self.map_options.grid(row=1, column=0, columnspan=2, sticky='NSEW')
        # Auto-Mapping Formatting Priority
        self.map_var = tk.IntVar(value=0)
        self.map_upper = tk.Radiobutton(self.map_frame, text='Longest string', variable=self.map_var, value=0)
        self.map_upper.grid(row=3, column=0)
        self.map_lower = tk.Radiobutton(self.map_frame, text='First instance', variable=self.map_var, value=1)
        self.map_lower.grid(row=3, column=1)
        # Check duplicates button
        self.map_button = tk.Button(self.map_frame, text='Auto-Map Descriptions', command=self.auto_map_desc)
        self.map_button.grid(row=4, column=0, columnspan=2, sticky='NSEW')
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
        self.data_can_scroll = tk.Scrollbar(self.can_frame, orient='vertical', command=self.data_can.yview)
        self.data_can_scroll.grid(row=1, column=3, sticky='NS')
        # endregion
        # endregion

        # region ================== 4.0 - Check Button ==================
        # Save Frame & Button
        self.save_frame = tk.Label(self.top_frame)
        self.save_frame.grid(row=2, column=0, sticky='NSEW')
        self.save_frame.columnconfigure(0, weight=1)
        self.save_button = tk.Button(self.save_frame, text='Check & Save Mappings:', height=3, command=self.map_desc)
        self.save_button.grid(row=0, column=0, sticky='EW')
        # Output Frame & Label
        self.output_frame = tk.Frame(self.top_frame)
        self.output_frame.grid(row=2, column=1, sticky='NSEW')
        self.output_frame.columnconfigure(0, weight=1)
        self.output_label = tk.Label(self.output_frame, text='', anchor='w')
        self.output_label.grid(row=0, column=0, sticky='NSW')
        # endregion

        # Disable elements initially
        self.disable_children(self.options_frame)

    # region 1.0 - Enable/Disable Canvas Functions
    def enable_canvas(self):
        self.main.desc_on = True
        self.on_off_warn_label.config(text='Please adjust formatting options and Check Descriptions')
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
        # Resets canvas
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
        self.data_can_scroll = tk.Scrollbar(self.can_frame, orient='vertical', command=self.data_can.yview)
        self.data_can_scroll.grid(row=1, column=3, sticky='NS')

        self.on_off_warn_label.config(text='Descriptions will not be adjusted. New COA cannot be generated without\n'
                                           'checking descriptions first, unadjusted raw COA will be exported instead.',
                                      fg='#8ace7e')

        self.disable_children(self.options_frame)

        self.main.colour(self.can_frame)

    # endregion

    # region 2.0 - Generate list of descriptions
    def flag_duplicates(self):
        # region 1) Get variables for if prefixes were set on, and if mappings were accepted
        pref_on = self.main.prefix_on
        pref_accept = self.main.prefix_accepted
        # endregion

        # region 2) Assign raw tb or prefixed tb to local variable
        if pref_on and pref_accept:
            self.imported_tb = self.main.prefixed_tb.copy()
        elif pref_on and not pref_accept:
            self.on_off_warn_label.config(text='Prefixed Codes selected but not mapped/saved correctly.'
                                               '\nPlease review Prefix Settings tab.', fg='#ff684c')
            return
        else:
            self.imported_tb = self.main.raw_tb.copy()
            self.on_off_warn_label.config(text='Raw TB Code descriptions checked for inconsistencies.', fg='#8ace7e')
        # endregion

        # region 3) Create another dataframe copy for editing down to codes with multiple descriptions
        multiple_desc = self.imported_tb.copy()
        multiple_desc['Desc.'] = multiple_desc['Desc.'].astype(str)  # NaN's > nan's, needed for filtering by uniques
        # Trim descriptions if selected
        if self.trim_var.get() == 1:
            multiple_desc['Desc.'] = multiple_desc['Desc.'].str.strip()
        # Adjust descriptions to upper or lower case if selected
        if self.case_var.get() == 1:
            multiple_desc['Desc.'] = multiple_desc['Desc.'].str.lower()
        elif self.case_var.get() == 2:
            multiple_desc['Desc.'] = multiple_desc['Desc.'].str.upper()
        # endregion

        # region 4) Filter for account codes with more than one description, field varies based on prefix selection
        code_field = 'Pref. Code' if self.main.prefix_on else 'Code'
        multiple_desc = multiple_desc.groupby(code_field).filter(lambda tb: tb['Desc.'].nunique() > 1)
        # endregion

        # region 5) Create unique field to use as filter, drop fields to leave unique instances of codes & desc.
        multiple_desc['Uniques'] = multiple_desc[code_field] + multiple_desc['Desc.']
        multiple_desc.drop_duplicates(subset=['Uniques'], inplace=True)
        multiple_desc.sort_values(code_field, inplace=True)
        drop_fields = ['Filename', 'Company', 'Code', 'Amount', 'Company New', 'Uniques'] if self.main.prefix_on \
            else ['Filename', 'Company', 'Amount', 'Uniques']
        multiple_desc.drop(columns=drop_fields, axis=1, inplace=True)
        # endregion

        # region 6) Assign description list to external variable in case GUI exceeds limits to correct manually
        self.desc_options = multiple_desc
        # endregion

        # region 7) Reset GUI canvas
        for widgets in self.data_can_sub_frame.winfo_children():
            widgets.destroy()
        # endregion

        # region 8) Update GUI depending on volume of duplicates found

        # 8.1) Mark Descriptions as correct if no inconsistencies found
        if multiple_desc.empty:
            self.dupe_limit = False
            self.main.desc_accepted = True
            self.imported_tb['Desc. New'] = self.imported_tb['Desc.']
            self.main.final_tb = self.imported_tb
            self.on_off_warn_label.config(text='No inconsistent descriptions found. Proceed to COA Mapping Tab.',
                                          fg='#8ace7e')

            # Disable GUI
            self.disable_children(self.map_frame)
            self.disable_children(self.can_frame)
            self.disable_children(self.save_frame)
            self.disable_children(self.output_frame)
        # 8.2) Display list of inconsistent descriptions if below GUI display limits
        elif int(multiple_desc[[code_field]].nunique()) <= 300:
            self.dupe_limit = False
            self.on_off_warn_label.config(text=str(int(multiple_desc[[code_field]].nunique())) +
                                          ' inconsistent descriptions found, please select mappings.',
                                          fg='#ffda66')
            # enable gui due to adjustments needed?
            self.enable_children(self.map_frame)
            self.enable_children(self.can_frame)
            self.enable_children(self.save_frame)
            self.enable_children(self.output_frame)

            # Convert duplicates df into list of lists, first element code, then list of desc. option to add to GUI
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
        # 8.3) If descriptions exceed GUI display limit, update warning that only automapping is available
        else:
            self.dupe_limit = True
            self.on_off_warn_label.config(text=str(int(multiple_desc[[code_field]].nunique())) +
                                          ' inconsistent descriptions found, exceeds display limits.'
                                          '\nPlease refer to Auto Map to correct duplicates.', fg='#ffda66')

            # enable gui due to adjustments needed?
            self.enable_children(self.map_frame)
            self.enable_children(self.can_frame)
            self.enable_children(self.save_frame)
            self.enable_children(self.output_frame)

        # endregion

    def auto_map_desc(self):
        # region 1) Reset mappings dataframe, get priority order from dictionary & code field dependent on prefixes
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
        # endregion

        # region 2) Automap GUI if descriptions list does not exceed GUI limits
        if not self.dupe_limit:
            # 2.1) Convert widgets in canvas to array format [[code name widget, desc. options widget]]
            canvas_widgets = self.data_can_sub_frame.winfo_children()
            widget_array = [canvas_widgets[x:x + 2] for x in range(0, len(canvas_widgets), 2)]

            # 2.2) Iterate through each individual code and their descriptions
            for row in widget_array:
                row: list  # Prevent pycharm false type error flag
                code = row[0].get()  # get code from widget array entry

                # 2.3) Get dataframe of the specific code, with its unique descriptions, and their TB period source
                mappings = self.desc_options[self.desc_options[code_field] == code]

                # 2.4) Loop three times for each of the PY, OP, CL tabs in order of priority selected
                for x in range(3):
                    if priority_check[x] in mappings['TB Period'].values:
                        # Filter to prioritised period
                        priority_map = mappings[mappings['TB Period'] == priority_check[x]]
                        # Convert to list
                        priority_map = priority_map['Desc.'].astype(str).tolist()
                        # Filter for either longest string or first instance listed based on option selections
                        if self.map_var.get() == 1:
                            desc_mapping = priority_map[0]
                        else:
                            desc_mapping = max(priority_map, key=len)
                        # Set option menu to automapped description
                        row[1].set(desc_mapping)
                        break
        # endregion

        # region 3) If GUI exceeds limits, selections are generated
        else:
            # 3.1) Get copy of imported TB data, either raw or prefixed
            mappings = self.desc_options

            # 3.2) Generate period priority order field in mapping df from 1 to 3, 4 as null placement
            mappings['Filter Column'] = 4
            mappings.loc[mappings['TB Period'] == priority_check[0], 'Filter Column'] = 1
            mappings.loc[mappings['TB Period'] == priority_check[1], 'Filter Column'] = 2
            mappings.loc[mappings['TB Period'] == priority_check[2], 'Filter Column'] = 3

            # 3.3) Filter for either longest string or first instance listed based on option selections
            mappings['String len'] = mappings['Desc.'].str.len()
            if self.map_var.get() == 1:
                mappings = mappings.sort_values(by=['Filter Column', code_field, 'String len', 'Desc.'],
                                                ascending=[True, True, False, True], axis=0)
            else:
                mappings = mappings.sort_values(by=['Filter Column', code_field, 'Desc.'],
                                                ascending=[True, True, True], axis=0)

            # 3.4) Drop duplicates and unneeded fields to get descriptions mapping dataframe
            mappings.drop_duplicates(subset=[code_field], keep='first', inplace=True)
            mappings.drop(columns=['TB Period', 'Filter Column', 'String len'], axis=1, inplace=True)
            self.desc_mappings = mappings

            # print('======= DESC. MAPPING - NO GUI DISPLAY =========')
            # print(self.desc_mappings)
            # print('Length of desc. Mapping: ' + str(len(tb)))
            # print('Unique Codes in desc. Mapping: ' + str(tb[code_field].nunique()))
        # endregion

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

    # region 4.0 - Save Descriptions
    def map_desc(self):
        # region 1) Reset final TB, error flags and set code field based on prefix settings
        self.main.final_tb = pd.DataFrame()
        error_flag = False
        code_field = 'Pref. Code' if self.main.prefix_on else 'Code'
        # endregion

        # region 2) Save Descriptions if GUI could be generated
        if not self.dupe_limit:
            # region 2.1) Convert widgets in canvas to array format [[code name widget, desc. options widget]]
            canvas_widgets = self.data_can_sub_frame.winfo_children()
            widget_array: list
            widget_array = [canvas_widgets[x:x + 2] for x in range(0, len(canvas_widgets), 2)]
            # endregion

            # region 2.2) Checks and flags rows that have not been mapped, updates error var
            for row in widget_array:
                colour_check = '#ff684c' if len(row[1].get().strip()) == 0 else '#8ace7e'
                row[0].config(readonlybackground=colour_check)
                if not error_flag:
                    error_flag = True if len(row[1].get().strip()) == 0 else False
            # endregion

            # region 2.3) Add TB to master Description TB if error checks pass
            if not error_flag:
                # Get account code & selected mapping, join to TB data on account code
                join = [[row[0].get(), row[1].get()] for row in widget_array]
                join_df = pd.DataFrame(join, columns=[code_field, 'Desc.'])
                tb_new_desc = pd.merge(self.imported_tb, join_df, on=code_field, how='left', suffixes=('', ' New'))

                # Fill new description field from original mappings, updating formatting if selected
                if self.case_var.get() == 1:
                    tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.lower(), inplace=True)
                elif self.case_var.get() == 2:
                    tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.upper(), inplace=True)
                else:
                    tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'], inplace=True)

                # Assign data to master finalised TB
                self.main.final_tb = tb_new_desc.copy()
            else:
                self.output_label.config(text='Descriptions mappings have not beem selected, highlighted in red.')
                self.master.tab(3, state='disabled')
                return
            # endregion
        # endregion

        # region 3) Save descriptions if no GUI was generated
        else:
            # 3.1) Join new description to TB data on account code
            tb_new_desc = pd.merge(self.imported_tb, self.desc_mappings, on=code_field, how='left',
                                   suffixes=('', ' New'))

            # 3.2) Fill new description field from original mappings, updating formatting if selected
            if self.case_var.get() == 1:
                tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.lower(), inplace=True)
            elif self.case_var.get() == 2:
                tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'].str.upper(), inplace=True)
            else:
                tb_new_desc['Desc. New'].fillna(tb_new_desc['Desc.'], inplace=True)

            # 3.3) Assign data to master finalised TB
            self.main.final_tb = tb_new_desc.copy()
        # endregion

        # region 4) Final error checks for data duplication
        desc_check = self.main.final_tb.groupby(code_field).filter(lambda x: x['Desc. New'].nunique() > 1)
        if len(desc_check) == 0:
            self.main.desc_accepted = True
            self.output_label.config(text='Trial balance updated with consistent descriptions', fg='#8ace7e')
            self.master.tab(3, state='normal')
        else:
            self.main.desc_accepted = False
            self.output_label.config(text='ERROR: Internal error, duplicates present after filtering.', fg='#ff684c')
            self.master.tab(3, state='disabled')
        # endregion

    # endregion

    # region misc. - Disable Children
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
