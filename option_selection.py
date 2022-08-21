import tkinter as tk
from tkinter import ttk
import pandas as pd
import re


class PrefixOptions:
    def __init__(self, master, main):
        self.master = master
        self.main = main
        self.mapping_selections = pd.DataFrame()
        self.widgets_State = 'disabled'

        # region Tkinter GUI
        # ================== 0.0 - Top Frame ==================
        self.top_frame = tk.Frame(master)
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.master.add(self.top_frame, text='Prefix Settings')
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(1, weight=1)

        # self.master.tab(1, state="disabled")

        # ================== 1.0 - Prefix On/Off ==================
        # Prefix on/off Frame
        self.on_off_frame = tk.Frame(self.top_frame)
        self.on_off_frame.grid(row=0, column=0, sticky='NSEW')

        for x in range(2):
            self.on_off_frame.columnconfigure(x, weight=1)

        self.on_off_label = tk.Label(self.on_off_frame, text='Add Prefixes & Company Name Updates:')
        self.on_off_label.grid(row=0, column=0, columnspan=2, sticky='W', padx=5)

        self.pref_var = tk.IntVar(value=0)
        self.on_button = tk.Radiobutton(self.on_off_frame, text='Yes', variable=self.pref_var,
                                        value=1, command=self.enable_canvas)
        self.on_button.grid(row=1, column=0, padx=5)

        self.off_button = tk.Radiobutton(self.on_off_frame, text='No', variable=self.pref_var,
                                         value=0, command=self.disable_canvas)
        self.off_button.grid(row=1, column=1, padx=5)

        self.warning_frame = tk.Frame(self.top_frame)
        self.warning_frame.grid(row=0, column=1, sticky='NSEW')

        self.warning_label = tk.Label(self.warning_frame,
                                      text='Prefixes not selected. Codes & Companies will be exported as is.')
        self.warning_label.grid(row=0, column=0)

        # ================== 1.0 - Options Frame ==================
        self.options_frame = tk.Frame(self.top_frame)
        self.options_frame.grid(row=1, column=0, sticky='NSEW')

        # ================== 2.0 - Company Options ==================

        # Primary Frame
        self.map_frame = tk.Frame(self.options_frame)
        self.map_frame.grid(row=1, column=0, sticky='NSEW')
        self.map_frame.columnconfigure(0, weight=1)

        self.map_label = tk.Label(self.map_frame, text='Auto-Map Options:')
        self.map_label.grid(row=0, column=0, columnspan=6, sticky='W', padx=5, pady=5)

        # ================== 2.1 - Company auto-map ==================

        # Substring Selections - Frame
        self.strings_frame = tk.Frame(self.map_frame)
        self.strings_frame.grid(row=1, column=0, sticky='EW', padx=5, pady=5)
        # Substring Selections - Label
        self.strings_label = tk.Label(self.strings_frame, text='Substring Selections:')
        self.strings_label.grid(row=0, column=0, columnspan=6,  sticky='W')

        # Substring Selections - "Map" Label
        self.string_map_label = tk.Label(self.strings_frame, text='Map')
        self.string_map_label.grid(row=1, column=0, sticky='W')
        # Substring Selections - Combobox
        self.string_select_list = ['All', 'Left', 'Right', 'Mid']
        self.string_select_box = ttk.Combobox(self.strings_frame, values=self.string_select_list, width=5,
                                              justify='center')
        self.string_select_box.current(0)
        self.string_select_box.bind('<<ComboboxSelected>>', self.substring_range)
        self.string_select_box.grid(row=1, column=1, sticky='W', padx=5)
        # Substring Selections - No. Entry 1
        self.string_entry_1 = tk.Entry(self.strings_frame, width=5, disabledbackground='#858585')
        self.string_entry_1['state'] = 'disabled'
        self.string_entry_1.bind('<KeyRelease>', self.substring_check)
        self.string_entry_1.grid(row=1, column=2)
        # Substring Selections - "-" Label
        self.string_hyphen_label = tk.Label(self.strings_frame, text=', ')
        # Substring Selections - No. Entry 2
        self.string_entry_2 = tk.Entry(self.strings_frame, width=5, disabledbackground='#858585')
        self.string_entry_2['state'] = 'disabled'
        self.string_entry_2.bind('<KeyRelease>', self.substring_check)
        # Substring Selections - "Characters" Label
        self.string_char_label = tk.Label(self.strings_frame, text='Characters')
        self.string_char_label.grid(row=1, column=5, sticky='W')

        # Case Formatting - Frame
        self.case_frame = tk.Frame(self.map_frame)
        self.case_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=5)

        self.case_label = tk.Label(self.case_frame, text='Case Formatting:')
        self.case_label.grid(row=0, column=0, columnspan=4, sticky='W')

        self.case_var = tk.IntVar()
        for x, case in zip(range(4), ['No Change', 'Title', 'Upper', 'Lower']):
            self.case_selection = tk.Radiobutton(self.case_frame, text=case,
                                                 variable=self.case_var, value=x)
            self.case_selection.grid(row=1, column=x, sticky='W')

        # Case Formatting - Trim Checkbutton
        self.trim_var = tk.IntVar(value=1)
        self.trim_check = tk.Checkbutton(self.case_frame, text='Trim Whitespace', variable=self.trim_var)
        self.trim_check.grid(row=2, column=0, sticky='W')

        # Automap Button
        self.map_button = tk.Button(self.case_frame, text='Automap Column(s)', command=self.automap_cols)
        self.map_button.grid(row=3, column=0, columnspan=4, sticky='EW')

        # Clear Button
        self.clear_button = tk.Button(self.case_frame, text='Clear Column(s)', command=self.clear_cols)
        self.clear_button.grid(row=4, column=0, columnspan=4, sticky='EW')

        # ================== 2.2 - Replace Text Format ==================
        # On/Off Map Companies - Frame
        self.replace_frame = tk.Frame(self.options_frame)
        self.replace_frame.grid(row=3, column=0, sticky='NSEW', padx=5, pady=5)
        self.replace_frame.columnconfigure(1, weight=1)

        self.replace_header_label = tk.Label(self.replace_frame, text='Custom String Replacement:')
        self.replace_header_label.grid(row=0, column=0, columnspan=2, sticky='W')

        self.replace_label = tk.Label(self.replace_frame, text='Replace:')
        self.replace_label.grid(row=1, column=0, sticky='W')

        self.replace_entry = tk.Entry(self.replace_frame)
        self.replace_entry.grid(row=1, column=1, sticky='EW', padx=5)

        self.with_label = tk.Label(self.replace_frame, text="With:")
        self.with_label.grid(row=2, column=0, sticky='W')

        self.with_entry = tk.Entry(self.replace_frame)
        self.with_entry.grid(row=2, column=1, sticky='EW', padx=5)

        self.exact_case_var = tk.IntVar(value=1)
        self.exact_case = tk.Checkbutton(self.replace_frame, text='Exact Case Only', variable=self.exact_case_var)
        self.exact_case.grid(row=3, column=0, columnspan=2, sticky='W')

        self.replace_button = tk.Button(self.replace_frame, text='Replace Text',
                                        command=self.replace_string)
        self.replace_button.grid(row=4, column=0, columnspan=2, sticky='NSEW')

        # ================== 3.0 - Prefix/Suffix Formatting ==================
        # Prefix/Suffix Frame
        self.suffix_prefix_frame = tk.Frame(self.options_frame)
        self.suffix_prefix_frame.grid(row=4, column=0, sticky='EW', padx=5)
        self.suffix_prefix_frame.columnconfigure(1, weight=1)

        self.suffix_prefix_header_label = tk.Label(self.suffix_prefix_frame, text='Adjust Code Format:')
        self.suffix_prefix_header_label.grid(row=0, column=0, sticky='W')

        # 'Prefixes/Suffixes' - Label
        self.suffix_prefix_label = tk.Label(self.suffix_prefix_frame, text='Prefix or Suffix:')
        self.suffix_prefix_label.grid(row=1, column=0, sticky='W')
        # 'Prefixes/Suffixes' - Button
        self.suffix_prefix_button = tk.Button(self.suffix_prefix_frame, text='Prefix', command=self.prefix_toggle)
        self.suffix_prefix_button.grid(row=1, column=1, sticky='EW', padx=5)

        # 'Prefix/Suffix Divider' - Label
        self.prefix_divider = tk.StringVar(value='')
        self.divider_label = tk.Label(self.suffix_prefix_frame, text='Divider:')
        self.divider_label.grid(row=2, column=0, sticky='W')
        # 'Prefix/Suffix Divider' - Entry
        self.prefix_entry = tk.Entry(self.suffix_prefix_frame, textvariable=self.prefix_divider)
        self.prefix_entry.grid(row=2, column=1, sticky='EW', padx=5)
        self.prefix_entry.bind('<KeyRelease>', self.prefix_toggle_display)

        # Display Example Code Format
        self.code_format = tk.StringVar(value='PREFIX' + str(self.prefix_divider.get()) + 'CODE')
        self.prefix_format_example = tk.Label(self.suffix_prefix_frame, text='Code Format Example:')
        self.prefix_format_example.grid(row=3, column=0, sticky='W')
        self.display_format_label = tk.Label(self.suffix_prefix_frame, textvariable=self.code_format)
        self.display_format_label.grid(row=3, column=1, sticky='EW')

        # ================== 4.0 - Main Canvas Frame ==================
        self.can_frame = tk.LabelFrame(self.top_frame)
        self.can_frame.grid(row=1, column=1, sticky='NSEW')
        for x in range(3):
            self.can_frame.columnconfigure(x, weight=1)
        self.can_frame.rowconfigure(1, weight=1)
        # ================== 4.1 - Header Canvas Frame ==================
        # Header Canvas
        self.head_can = tk.Canvas(self.can_frame, height=23)
        self.head_can.grid(row=0, column=0, columnspan=3, sticky='EW')
        self.head_can.bind('<Configure>', self.frame_width)
        # Header Canvas Sub-Frame
        self.head_can_sub_frame = tk.Frame(self.head_can)
        self.head_can_sub_frame.bind('<Configure>', self.config_frame)
        # Header canvas Window
        self.head_can_window = self.head_can.create_window(0, 0, anchor='nw', window=self.head_can_sub_frame)

        # NEW BUTTON ON/OFF
        for x in range(3):
            self.head_can_sub_frame.columnconfigure(x, weight=1)

        # 'Imported Comp.'
        self.import_label = tk.Label(self.head_can_sub_frame, text='Imported Comp.')
        self.import_label.grid(row=0, column=0, sticky='NSEW')

        # 'New Comp. Mappings'
        self.comp_map_var = tk.IntVar(value=0)
        self.comp_map_button = tk.Button(self.head_can_sub_frame, text='New Comp. Mappings',
                                         command=lambda: self.button_on_off(self.comp_map_button, self.comp_map_var))
        self.comp_map_button.grid(row=0, column=1, sticky='NSEW')

        # 'New Comp. Mappings'
        self.pref_map_var = tk.IntVar(value=0)
        self.pref_map_button = tk.Button(self.head_can_sub_frame, text='Prefix/Suffix',
                                         command=lambda: self.button_on_off(self.pref_map_button, self.pref_map_var))
        self.pref_map_button.grid(row=0, column=2, sticky='NSEW')

        # ================== 4.2 - Data Canvas Frame ==================
        self.data_can = tk.Canvas(self.can_frame, bg='#BDCDFF')
        self.data_can.grid(row=1, column=0, columnspan=5, sticky='NSEW')
        self.data_can.bind('<Configure>', self.frame_width)
        self.data_can.rowconfigure(0, weight=1)
        # Main Canvas Sub-Frame
        self.data_can_sub_frame = tk.Frame(self.data_can)
        for col in range(3):
            self.data_can_sub_frame.columnconfigure(col, weight=1)
        self.data_can_sub_frame.bind('<Configure>', self.config_frame)
        # Main Canvas Window
        self.data_can_window = self.data_can.create_window(0, 0, anchor='nw', window=self.data_can_sub_frame)
        # Scrollbar
        self.data_can_scroll = tk.Scrollbar(self.can_frame, orient="vertical", command=self.data_can.yview)
        self.data_can_scroll.grid(row=1, column=5, sticky='NS')

        #  ================== 5.0 - Check/Load Prefixes ==================

        self.load_frame = tk.Frame(self.top_frame)
        self.load_frame.grid(row=2, column=0, sticky='NSEW')
        self.load_frame.columnconfigure(0, weight=1)

        self.load_button = tk.Button(self.load_frame, text='Check & Save Mappings:', height=3,
                                     command=self.map_prefixes)
        self.load_button.grid(row=0, column=0, sticky='EW')
        self.load_button.columnconfigure(0, weight=1)

        self.load_frame_2 = tk.Frame(self.top_frame)
        self.load_frame_2.grid(row=2, column=1, sticky='NSEW')
        self.load_frame_2.columnconfigure(0, weight=1)
        self.load_frame_2.rowconfigure(0, weight=1)

        self.load_label = tk.Label(self.load_frame_2, text='', anchor='w')
        self.load_label.grid(row=0, column=0, sticky='NSW')
        # endregion

        # Disable elements initially
        # self.disable_children(self.options_frame)
        # self.disable_children(self.head_can)
        # self.disable_children(self.load_frame)
        # self.disable_children(self.load_frame_2)

    # region Canvas Display Functions
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

    # region Enable/Disable Tab
    def enable_canvas(self):
        # Generate canvas widgets from companies imported, add warning if above suggested limit
        companies = sorted(self.main.raw_company, key=str.lower)
        if len(companies) > 150:
            self.warning_label.config(text='Warning: ' + str(len(companies)) + ' companies in data. Volumes this\n'
                                      'large may be impractical to prefix manually due to user interface limits.\n'
                                      'Advise automapping fields or importing less files at a time.',
                                      fg='#ffda66')
        else:
            self.warning_label.config(text='Please add Company/Prefix mappings then press Check & Save Mappings.',
                                      fg='#ffda66')

        for x in companies:
            y = companies.index(x)

            old_co = tk.Entry(self.data_can_sub_frame, font=('Segoe UI', '10'))
            old_co.insert(0, x)
            old_co.grid(row=y, column=0, sticky='NSEW', padx=1, pady=1)
            old_co.config(highlightthickness=2, borderwidth=2)
            old_co.config(state='readonly')

            new_co = tk.Entry(self.data_can_sub_frame, font=('Segoe UI', '10'))
            new_co.grid(row=y, column=1, sticky='NSEW', padx=1, pady=1)
            new_co.config(highlightthickness=2, borderwidth=2)

            prefix = tk.Entry(self.data_can_sub_frame, font=('Segoe UI', '10'))
            prefix.grid(row=y, column=2, sticky='NSEW', padx=1, pady=1)
            prefix.config(highlightthickness=2, borderwidth=2)

        # Enable canvas widgets
        self.main.prefix_on = True
        self.enable_children(self.options_frame)
        self.enable_children(self.head_can)
        self.enable_children(self.load_frame)
        self.enable_children(self.load_frame_2)

        # Enable specific to substring selections
        selection = self.string_select_box.get()
        entry_1_state = 'normal' if selection != 'All' else 'disabled'
        entry_2_state = 'normal' if selection == 'Mid' else 'disabled'
        button_state = 'normal' if selection == 'All' else 'disabled'
        self.string_entry_1['state'] = entry_1_state
        self.string_entry_2['state'] = entry_2_state
        self.map_button['state'] = button_state

    def enable_children(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            widget_type = child.winfo_class()
            if widget_type not in ('Frame', 'Labelframe'):
                child.configure(state='normal')
            else:
                # 2) Repeats loops with sub_children of widget
                self.enable_children(child)

    def disable_canvas(self):
        # Clears warning label
        self.warning_label.config(text='Prefixes not selected. Codes & Companies will be exported as is.',
                                  fg='#8ace7e')

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
        for col in range(3):
            self.data_can_sub_frame.columnconfigure(col, weight=1)
        self.data_can_sub_frame.bind('<Configure>', self.config_frame)
        # Main Canvas Window
        self.data_can_window = self.data_can.create_window(0, 0, anchor='nw', window=self.data_can_sub_frame)

        self.main.prefix_on = False
        self.disable_children(self.options_frame)
        self.disable_children(self.head_can)
        self.disable_children(self.load_frame)
        self.disable_children(self.load_frame_2)

        self.main.colour(self.can_frame)

    def disable_children(self, parent):
        # 1) loop through each child of widget except for enable/disable frame
        for child in parent.winfo_children():
            widget_type = child.winfo_class()
            if widget_type not in ('Frame', 'Labelframe'):
                child.configure(state='disable')
            else:
                # 2) Repeats loops with sub_children of widget
                self.disable_children(child)
    # endregion

    # region Substring Functions
    def substring_range(self, _):
        self.string_entry_1.delete(0, tk.END)
        self.string_entry_2.delete(0, tk.END)

        selection = self.string_select_box.get()

        entry_1_state = 'normal' if selection != 'All' else 'disabled'
        entry_2_state = 'normal' if selection == 'Mid' else 'disabled'
        button_state = 'normal' if selection == 'All' else 'disabled'

        self.string_entry_1['state'] = entry_1_state
        self.string_entry_2['state'] = entry_2_state
        self.map_button['state'] = button_state

        if selection == 'Mid':
            self.string_hyphen_label.grid(row=1, column=3)
            self.string_entry_2.grid(row=1, column=4)
        else:
            self.string_hyphen_label.grid_forget()
            self.string_entry_2.grid_forget()

    def substring_check(self, _):
        try:
            int(self.string_entry_1.get())
            state = 'normal' if int(self.string_entry_1.get()) != 0 else 'disabled'
            self.map_button['state'] = state
        except ValueError:
            self.map_button['state'] = 'disabled'
            return  # Prevents button enabling if second value is correct format

        if self.string_select_box.get() == 'Mid':
            try:
                int(self.string_entry_2.get())
                state = 'normal' if int(self.string_entry_1.get()) != 0 \
                        and int(self.string_entry_2.get()) != 0 else 'disabled'
                self.map_button['state'] = state
            except ValueError:
                self.map_button['state'] = 'disabled'
    # endregion

    def button_on_off(self, button, var):
        if button.config('relief')[-1] == 'sunken':
            button.config(relief='raised')
            var.set(0)
            print('Button var:' + str(var.get()))

            col = button.grid_info()['column']
            print('Button Col:' + str(col))

            for child in self.data_can_sub_frame.winfo_children():
                child: tk.Entry()
                if child.grid_info()['column'] == col:
                    print('Child Grid Info:' + str(child.grid_info()['column']))
                    child.config(highlightthickness=2, highlightbackground="white")

        else:
            button.config(relief='sunken')
            var.set(1)
            print('Button var:' + str(var.get()))

            col = button.grid_info()['column']
            print('Button Col:' + str(col))

            for child in self.data_can_sub_frame.winfo_children():
                child: tk.Entry()
                if child.grid_info()['column'] == col:
                    print('Child Grid Info:' + str(child.grid_info()['column']))
                    child.config(highlightthickness=2, highlightbackground="#64C75F")

    # region Automap/Clear Mappings Functions
    def automap_cols(self):
        # 1) Get column selections
        columns = [self.comp_map_var, self.pref_map_var]

        # 2) Loop through columns if selected
        for col in columns:
            x = columns.index(col) + 1  # Determine column to map to

            if col.get() == 1:
                # 3) Maps company entry to corresponding fields
                company = str()
                for child in self.data_can_sub_frame.winfo_children():
                    child: tk.Entry()  # Must explicitly declare type to prevent attribute error as frame is null

                    # 4) Gets company in column 1
                    if child.grid_info()["column"] == 0:
                        company = child.get()

                    # 5) Map to selected field
                    if child.grid_info()["column"] == x:

                        # 6) Gets substring of company if option was selected
                        if self.string_select_box.get() != 'All':
                            characters = int(self.string_entry_1.get())
                            if self.string_select_box.get() == 'Left':
                                company = company[:characters]
                            elif self.string_select_box.get() == 'Right':
                                company = company[-characters:]
                            elif self.string_select_box.get() == 'Mid':
                                characters_mid = int(self.string_entry_2.get())
                                company = company[characters - 1:characters + characters_mid - 1]

                        # 7) Reformat string if option was selected
                        if self.case_var.get() != 0:
                            if self.case_var.get() == 1:
                                company = company.replace("'", "").title()
                            elif self.case_var.get() == 2:
                                company = company.upper()
                            elif self.case_var.get() == 3:
                                company = company.lower()

                        # 8) Trim if option was selected
                        if self.trim_var.get() == 1:
                            company = company.strip()

                        # 9) Map to new field
                        child.delete(0, tk.END)
                        child.insert(0, company)

    def clear_cols(self):
        # 1) Get column selections
        columns = [self.comp_map_var, self.pref_map_var]

        # 2) Loop through columns and reset entries
        for col in columns:
            x = columns.index(col) + 1  # Determine column to map to
            if col.get() == 1:
                for child in self.data_can_sub_frame.winfo_children():
                    child: tk.Entry()  # Must explicitly declare type to prevent attribute error as frame is null
                    if child.grid_info()["column"] == x:
                        child.delete(0, tk.END)
    # endregion

    # Replace String
    def replace_string(self):
        # 1) Get string replacement selections
        original_string = self.replace_entry.get()
        replacement_string = self.with_entry.get()

        # 2) Get column selections
        columns = [self.comp_map_var, self.pref_map_var]

        # 3) Loop through columns and replace string
        for col in columns:
            x = columns.index(col) + 1  # Determine column to map to
            if col.get() == 1:
                for child in self.data_can_sub_frame.winfo_children():
                    child: tk.Entry()  # Must explicitly declare type to prevent attribute error as frame is null
                    if child.grid_info()["column"] == x:
                        company = str(child.get())

                        # 4) Case sensitive replacement setting
                        if self.exact_case_var.get() != 1:
                            string_replacer = re.compile(re.escape(original_string), re.IGNORECASE)
                        else:
                            string_replacer = re.compile(re.escape(original_string))

                        new_string = string_replacer.sub(replacement_string, company)

                        # 5) Trim if option was selected
                        if self.trim_var.get() == 1:
                            new_string = new_string.strip()

                        child.delete(0, tk.END)
                        child.insert(0, new_string)

    # region Prefix/Suffix Functions
    def prefix_toggle(self):
        if self.suffix_prefix_button.config('text')[-1] == 'Prefix':
            self.suffix_prefix_button.config(text='Suffix')
            self.code_format.set('CODE' + str(self.prefix_divider.get()) + 'SUFFIX')
        else:
            self.suffix_prefix_button.config(text='Prefix')
            self.code_format.set('PREFIX' + str(self.prefix_divider.get()) + 'CODE')

    def prefix_toggle_display(self, _):
        if self.suffix_prefix_button.config('text')[-1] == 'Prefix':
            self.code_format.set('PREFIX' + str(self.prefix_divider.get()) + 'CODE')
        else:
            self.code_format.set('CODE' + str(self.prefix_divider.get()) + 'SUFFIX')
    # endregion

    # Save Mappings
    def map_prefixes(self):
        # 1) Flags created for blank companies & no prefixes mapped
        self.main.prefix_accepted = False
        company_error = False
        prefix_error = False

        # 2) Canvas widget list is generated and converted into 3 column nested list
        canvas_widgets = self.data_can_sub_frame.winfo_children()
        widget_array = [canvas_widgets[x:x + 3] for x in range(0, len(canvas_widgets), 3)]

        # 3) Widget contents are checked for valid entries & colours/labels updated
        for row in widget_array:
            row: tk.Entry()  # Suppresses false flag evaluation error with pycharm
            # 3.1) Check for blank company mappings
            if len(row[1].get().strip()) == 0:
                company_error = True
                row[1].config(bg='#ff684c')
            else:
                row[1].config(bg='#8ace7e')
            # 3.2) Check for blank prefix mappings
            if len(row[2].get().strip()) == 0:
                prefix_error = True
                row[2].config(bg='#ffda66')
            else:
                row[2].config(bg='#8ace7e')

        # 4) Label is updated dependent on errors found or lack of
        error_status = str()
        comp_string = 'ERROR: Blank Companies found, please map all highlighted entries.'
        prefix_string = 'Caution: Prefixes were left blank.'
        correct_import = 'Prefixed Codes Mapped: Proceed to next tab'
        error_colour = '#FFFFFF'
        if not company_error:
            error_status = correct_import if not prefix_error else correct_import + '\n' + prefix_string
            error_colour = '#8ace7e' if not prefix_error else '#ffda66'
        elif company_error:
            error_status = comp_string if not prefix_error else comp_string + '\n' + prefix_string
            error_colour = '#ff684c'
        self.load_label.config(text=error_status, fg=error_colour)

        # 5) Join TB data if all companies mapped
        if not company_error:

            # 6) Assign raw TB data to local variables
            tb = self.main.raw_tb

            # 7) Use .get() to generate dataframe of values in widgets if no major errors found
            widget_array: list  # Suppresses false flag evaluation error with pycharm
            prefix_maps = pd.DataFrame([[row[0].get(), row[1].get(), row[2].get()] for row in widget_array],
                                       columns=['Company', 'Company New', 'Prefix'])

            # 8) Join tb with prefix mappings
            tb_join = pd.merge(tb, prefix_maps, on='Company')

            # 9) Create prefixed account code field using prefix/suffix format settings
            divider = str(self.prefix_divider.get())
            if self.suffix_prefix_button['text'] != 'Prefix':
                tb_join['Pref. Code'] = tb_join['Code'] + divider + tb_join['Prefix']
            else:
                tb_join['Pref. Code'] = tb_join['Prefix'] + divider + tb_join['Code']
            # print(tb_join)

            # 10) Rename and drop fields no longer needed
            tb_join.drop(columns=['Prefix'], axis=1, inplace=True)
            tb_join = tb_join.reindex(columns=['Filename', 'TB Period', 'Company', 'Code', 'Desc.', 'Amount',
                                               'Company New', 'Pref. Code'])

            self.main.prefixed_tb = tb_join
            self.main.prefix_accepted = True

        print('\n======== PREFIXED TB ========')
        print(self.main.prefixed_tb)
