# Trial Balance Converter Readme
# Contents
[1.0 – Overview](#overview)

[2.0 – Import Selection](#import)

[3.0 – Prefix Settings](#prefix)

[4.0 – Description Settings](#desc)

[5.0 – Chart of Accounts Generation](#coa)

[6.0 – Export Data](#export)



# <a name="overview"></a>1.0 – Overview:

### 1.1 - Preface
This program is designed for the checking & correction of financial trial balance (TB) data in .xlsm files for the purpose of financial auditing. It is currently being considered by BDO LLP for integration into the data analytics audit process. However, it should be noted that this program has been developed entirely independent of the company outside of business hours, and adapted to the specific TB template of this company using manually generated dummy data.

Typically, audit clients will perform an export of their raw system TB data, and fill out the standard audit .xlsm template so that it may be imported into a dashboard. There are often significant errors when a client fills out these templates, which can result in major discrepencies such as the TB data not aligning with its corresponding journal data on a dashboard. This program is designed to thoroughly check through TB data and rapidly correct numerous common errors, including: 

- Preliminary checks for missing key & secondary data, and value fields containing non-numeric entries
- Standardisation of company naming syntax and prefixing/suffixing of account codes to isolate by entity
- Correction of inconsistent account descriptions for the same account code
- Generation of an updated chart of accounts without duplicates or inconsistencies
- Remapping of chart of accounts in instances where non-standard template mappings are present
- Export of the company(s) data, consolidated into one file if multiple .xlsm files were input

**NOTE:** The files [saved here](https://github.com/dwrlewis/Trial-Balance-Converter/tree/master/Test%20Files) match the format of the .xlsm template this program was designed for, but are minimum reproductions. This is because the original template contains a large number of macros that were created internally by BDO LLP. As such, the templates provided have been entirely stripped of any company specific info. The program did not need adjusting to accommodate for this, as the only dependency is the naming of the column headers and tab names.

### 1.2 - Interpreter Settings
This program was generated in Python 3.8.0 using the Pycharm IDE with the following interpreter settings:

|***Package***|***Version***|
| - | - |
|Et-xmlfile|1.1.0|
|Numpy|1.22.4|
|Openpyxl|3.0.10|
|Pandas|1.4.2|
|Pip|21.1.2|
|Python-datautil|2.8.2|
|Pytz|2022.1|
|Setuptools|57.0.0|
|Six|1.16.0|
|Wheel|0.36.2|



# <a name="import"></a>2.0 – Import Selection:

### 2.1 - File Path & Import
The converter can be used for checking and correcting an individual .xlsm template or multiple simultaneously, the latter of which will result in all data being consolidated into a single file for export. The User Interface opens in the Import Selection tab. Select the import directory in the top left of this tab, which will automatically display a list of .xlsm files in the selected folder.

The data to import can be selected down to the individual tabs. For example, one file may have its Prior, Closing and COA imported, whilst another may only have a Closing imported. The header columns are also selectable buttons to enable/disable the import for an entire tab set, as are the Filenames which enable/disables the import for that particular file:

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/122afb7b9c98e57406c37bdbac849a3f104898aa/Readme%20Gifs/1%20-%20Tab%20Selection.gif)

The Filter Null Amounts option is designed for unusually large system exports containing every possible code in a system, even ones that have seen no movement in the year end period being audited. As such, this can be used to remove all irrelevant TB lines for each period, reducing both load time and redundant error flags.

Once selections are made, "Load Trial Balances" can be selected in the bottom left to begin importing the selected data.

### 2.2 - Import Results and Error Flags
Once all the files have been checked, the user interface colours will update to display any immediate errors it may have flagged in each files tabs:

- Green highlights mean that there were no errors found in the data tab.
- Yellow highlights mean there are minor errors present. This can include things like null descriptions or amount fields where zeroes may have been left as null entries.
- Red highlights mean this tab of data could not be imported. This can be a result of missing company or account codes, non-numeric data in the amount field, or miscellaneous import errors such as missing tabs or column headers, which would indicate the client has made major adjustments to the template.

Hovering over a particular cell containing an error will display a list of all the errors that were found whilst try to import the data from that particular tab. It is also possible to change selections press Load Trial Balances again, if for example, you decide a particular dataset can be left out entirely based on errors flagged in a particular tab. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/2%20-%20Tab%20Error%20Checking.gif)

Once the imported data has been checked for errors and deemed adequate, move to the ‘Prefix Settings’ tab of the user interface.


# <a name="prefix"></a>3.0 – Prefix Settings:

### 3.1 - Selecting Company & Prefix Corrections
The prefix settings tab is the first set of corrections to make to a TB. In the top left of this tab, there is a selection for this option. Note that whilst it is not mandatory to perform these checks, not doing so will disable generating a new COA in a later tab, as it is dependent on corrections made in this section.

Once the selection is made, it will generate a list of all unique company names found across all imported data files in the interface. This is intended to flag inconsistencies in how companies have been entered across different tabs and files. For example, “Alpha Company Limited” might be entered as “Alpha Ltd” in a different tab of data, which would cause alignment errors when loaded into a financial analyser dashboard.

The user interface here effectively serves the same role as an excel style mapping document. The ‘New Comp. Mappings’ field is what the companies will be renamed as in the export, whilst the ‘Prefix/Suffix’ field will be added to all account codes for that respective company.

New mappings can be entered manually the same as in an excel, but it is also possible to automatically map data using the options on the left of the user interface. This is a more viable alternative for large numbers of companies.

### 3.2 - Additional Options
Both the ‘New Comp. Mappings’ and ‘Prefix/Suffix’ headers can be selected the same way as column selection in excel, which turns the border green and allows options adjustments to be applied.

By default, the Automap Column(s) function is set to use the whole string but can also be adjusted to draw from the left, mid, or right of the Imported Company field in the same way as excel. 

There are also casing adjustments for Upper, Lower, and Title, as well as trimming whitespace from the field, and a replace function that can be limited by casings. Below is an example of correcting the imported companies:

1) The Mid function is used to take all text past "Company", and convert into title case for consistency

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/3%20-%20Company%20Format%20Map%20+%20Substring.gif)

2) Instances of ‘limited’ in all cases are replaced with ‘Ltd’. Manual corrections are then made for the remaining companies

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/4%20-%20Company%20Replace.gif)

3) For the prefixes, a mid function is used with upper case to take 5 characters from the company field to generate the prefixes

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/01b7ddf9fcb31e8ad4af3a537101d6c35c372b95/Readme%20Gifs/5%20-%20Prefix%20Map.gif)

### 3.3 - Prefix/Suffix Formatting Options
When inputting the prefix, dividers should not be added manually. For example, ‘Company Alpha’ should have its prefix input as ‘ALPHA’ rather than ‘ALPHA\_’. The divider is instead set in the bottom left section of the options, should one be needed. It is also possible to set the formatting to suffixes instead. An example of the format of the outputted codes is also displayed in the GUI:

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/6%20-%20Prefix%20Divider%20v2.gif)

For example, setting a prefix to ‘ALPHA’, maintaing prefix format, and the delimiter as a ‘__’, will result in the output codes like ‘ALPHA__1000’.

### 3.4 - Large Company Volumes
In instances where the number of companies are excessively large (>150) a warning flag will be added to the GUI advising the use of automapping. Extremely large numbers of companies can cause the GUI of tkinter to become impactically slow due to the number of widgets generated. In these instances it is advised to perform corrections one file at a time.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/672c15887f95623cfec875682f37be47fa257c3f/Readme%20Images/Prefix%20Limit.png)

### 3.5 - Saving Mappings
When all mappings have been filled out, pressing ‘Check & Save Mappings:’ will either mark all fields in green if filled out correctly, or flag up an empty field. Adding prefixes is not mandatory for all companies, and will only flag up a warning, but remapping company names must be completed to flag this section as complete. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/7%20-%20Saving%20Mappings%20v2.gif)

When all mappings are confirmed, move to the ‘Description Settings’ tab.


#  <a name="desc"></a>4.0 – Description Settings:

### 4.1 - Selecting Company & Prefix Corrections
Similar to the prefix tab, inconsistent descriptions do not have to be corrected, but generating a new COA is dependent on both the completion of the prefix tab as well as this section to prevent generating duplicate codes. Selecting yes enables the ‘Check Descriptions’ Menu.

When checking for account codes with inconsistent descriptions, it is also possible to reduce the number of inconsistencies using the options. If there is a high volume of inconsistent descriptions, this can be corrected by trimming descriptions, as well as adjusting their formatting to lower or upper case since this is common formatting issue between tabs. Title case is not available due to the unpredictable impact of special characters on this function.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/8%20-%20Load%20Descs%20and%20manual%20map.gif)

When ‘Check Descriptions’ is pressed, a list of account codes and their description options will be generated. If none are present, a notification will pop up prompting to move to the COA Regeneration tab. Otherwise, the list of inconsistent code descriptions will be shown.

### 4.2 - Automapping Descriptions
The Descriptions column contains a drop down of all possible mapping options for a specific code. If there is a significant volume of codes, it is possible to AutoMap the descriptions in priority order.

For example, if all codes in the CL (Closing) tab appear to be correct, whilst the PY (Prior Year) and OP (Opening) have clear spelling errors, then the AutoMap could be set to ‘CL > OP > PY’ prioritisation order. This will automatically select all available descriptions in the Closing tab first, and if not present defer to the Opening tab, then the Prior tab.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/9%20-%20Automap%20Desc.gif)

Prioritisation order can also be set within an individual tab itself. By default, it is set to take the longest available string in a tab, but it is also possible to select first instance of a string if this is needed. Manual adjustments are also still possible after automapping if there is a specific exception to the rule.

When ‘Check & Save Mappings’ is selected, it will automatically flag up blank description selections the same way as in the prefix settings tab. Otherwise, if all selections are made, move on to the COA Regeneration tab.



#  <a name="coa"></a>5.0 – Chart of Accounts Generation:
### 5.1 - Pre-requisites to Generate a New COA
It is only possible to regenerate a chart of accounts if both the Prefix Settings and Description Settings Tabs have been completed. This is because the data must have had all errors relating to these tabs purged from the trial balance, or this section will regenerate the same errors in the COA and cause inconsistencies when loaded into a financial analyser.

### 5.2 - Selecting Mapping Sources
When generating a new COA, it is possible to isolate the potential mappings to just its sources files COA data. If this is selected, then it will likely result in a large number of unmapped codes if the original COA was incomplete, but is useful for assuring data consistency of a specific companies’ mappings.

Setting ‘Extend mappings to all TBs’ will first search for a code mapping in the source file as in the option above, but if not found, will defer to any other trial balance COA’s that were imported for an alternative mapping. This is particularly useful when all companies are known to use the same mappings across entities, but each files COA only contains codes with movement during the year.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/10%20-%20COA%20Check.gif)

### 5.3 - Non-standard Mappings
The original .xlsm template had a limited number of COA mappings to draw from, with deviation of any kind (including case adjustments, spaces etc.) resulting in errors on upload to the dashboard. When the COA is regenerated and mapped, it will check for any mappings that are not standard selections and add these to the GUI.

Approximate mapping is available to correct this should the volume be too excessive to do so manually. For example, if a trial balance include an ‘A1 INTAN. ASSET’ mapping, it would infer from the left string that this should be mapped to ‘A1 – Intangible Assets’. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/11%20-%20COA%20Auto-map.gif)

Alternatively, these custom mappings can be maintained, as it is possible to add to the standard mappings field in the original .xlsm template for exceptional circumstances.

Once all non-standard codes are corrected and ‘Check & Save Mappings’ is selected, move on to the Export Data tab.



#  <a name="export"></a>6.0 – Export Data:

### 6.1 - Review Data
This tab will display the data input, adjustments made, and output for both the trial balance data and chart of accounts. If any sections have not been completed this will be flagged up accordingly.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/1126ee3117ba405bcaa80dcd7ed60f6c25758c2c/Readme%20Gifs/12%20-%20Review%20Checking%20v2.gif)

The data can be exported in several formats, including the following:

- Raw TB/COA – Exports the original unedited data (aside from filtering 0 values on import), but consolidated by each period tab.
- Adjusted TB/COA – Exports the edited data, including the prefixes, updated descriptions, and regenerated COA if available, consolidated by each period tab. It is also possible to remove all unmapped COA entries from the export.
- Detailed Meta TB/COA – Mainly used for assurance testing, exports a file including the hidden columns not normally present in regular exports, showing each stage of a column conversion to flag up any potential errors that occurred.

Select an export directory and export the file, which will be saved as ‘Trial Balance Export.xlsx’. Note that any file in the selected directory with this name will be overwritten. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/bf7c082b04f5f71307396d05791e142afc4eea9c/Readme%20Gifs/13%20-%20Excel%20Export.gif)

The export template is saved in .xlsx format for simplicity, as exporting directly to the original .xlsm template would create an unecessary dependency when the data can be directly copy/pasted manually.
