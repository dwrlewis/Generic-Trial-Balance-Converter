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
This program is designed for the checking & correction of trial balance (TB) data in .xlsm formatted standard template. Audit clients will typically need to convert their raw system TB exports into a standard format if it is to be uploaded into a financial analyser dashboard, but this can often result in discrepancies due to human error when attempting to standardise the data.
This can result in significant data reconciling discrepancies when added to a dashboard. This program is designed to thoroughly check through standardised TB data and rapidly correct numerous common errors, including: 

- Preliminary checks for missing key & secondary data, and value fields containing non-numeric entries
- Standardisation of company naming syntax and prefixing/suffixing of account codes to isolate by entity
- Correction of inconsistent account descriptions for the same account code
- Generation of an updated chart of accounts without duplicates or inconsistencies
- Remapping of chart of accounts in instances where non-standard template mappings are present

Export of the company(s) data, consolidated into one file if multiple .xlsm files were input
The files [saved here](https://github.com/dwrlewis/Trial-Balance-Converter/tree/master/Test%20Files) are generic minimum reproductions of a typical trial balance template this program would be designed for. 

**NOTE:** 
This program is now currently being considered by BDO LLP for integration into the data analytics audit process. However, it has been developed entirely independent of the company outside of business hours as a proof of concept and is now being adjusted to their specific template format on a separate repository.

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
The converter can be used for checking and correcting an individual .xlsm template or multiple simultaneously, the latter of which will result in all data being consolidated into a single file for export. The User Interface opens in the “Import Selection” tab. Select the import directory in the top left of this tab, which will automatically display a list of all the .xlsm files in the selected folder.

The data to import can be selected down to the individual tabs. For example, one file may have its Prior, Closing and COA imported, whilst another may only have a Closing imported. The header columns are also selectable buttons to enable/disable the import for an entire tab set, as are the Filenames which enable/disables the import for that particular file:

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/1%20-%20File%20Select.gif)

The Filter Null Amounts option is designed for unusually large system exports containing every possible code in a system, even ones that have seen no movement in the year end period being audited. As such, this can be used to remove all irrelevant TB lines for each period, reducing both load time and redundant error flags.

Once selections are made, "Load Trial Balances" can be selected in the bottom left to begin importing the selected data.

### 2.2 - Import Results and Error Flags
Once all the files have been checked, the user interface colours will update to display any immediate errors it may have flagged in each file’s tabs:

- Green highlights mean that there were no errors found in the data tab.
- Yellow highlights mean there are minor errors present. This can include things like null descriptions or amount fields where zeroes may have been left as null entries.
- Red highlights mean this tab of data could not be imported. This can be a result of missing company or account codes, non-numeric data in the amount field, or miscellaneous import errors such as missing tabs or column headers, which would indicate the client has made major adjustments to the template.

Hovering over a particular cell will display a list of all the errors that were found whilst try to import the data from that particular tab. It is also possible to change selections by pressing “Load Trial Balances” again, If for example, you decide a particular dataset can be left out entirely based on its errors.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/1.1%20-%20File%20Error.gif)

Once the imported data has been checked for errors and deemed adequate, move to the “Prefix Settings” tab of the user interface.


# <a name="prefix"></a>3.0 – Prefix Settings:

### 3.1 - Selecting Company & Prefix Corrections
The prefix settings tab is the first set of corrections to make to a TB. In the top left of this tab, there is a selection for this option. Note that whilst it is not mandatory to perform these checks, not doing so will disable generating a new COA, as it is dependent on corrections made here.

Once the selection is made, it will generate a list of all unique company names found across all imported data files. This is intended to flag inconsistencies in how companies have been entered across different tabs and files. For example, “Alpha Company Limited” might be entered as “Alpha Ltd” in a different tab of data, which would cause alignment errors when loaded into a dashboard.

The user interface here effectively serves the same role as an excel style mapping document. The “New Comp. Mappings” field is what the companies will be renamed as in the export, whilst the “Prefix/Suffix” field will be added to all account codes for that respective company.

New mappings can be entered manually the same as in an excel, but it is also possible to automatically map data using the options on the left of the user interface. This is a more viable alternative for large numbers of companies.

### 3.2 - Additional Options
Both the “New Comp. Mappings” and “Prefix/Suffix” headers can be selected the same way as column selection in excel, which turns the border green and allows options adjustments to be applied.

By default, the “Automap Column(s)” function is set to use the whole string but can also be adjusted to draw from the Left, Mid, or Right of the “Imported Company” field in the same way as excel. 

There are also casing adjustments for Upper, Lower, and Title, as well as trimming whitespace from the field, and a replace function that can be limited by casings. Below is an example of correcting the imported companies and adding prefixes:

1) The Mid function is used to take all text past "Company", and convert into title case for consistency

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/2.0%20-%20Comp%20Title.gif)

2) Instances of ‘limited’ in all cases are replaced with ‘Ltd’. Manual corrections are then made for the remaining companies

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/2.1%20-%20Comp%20Ltd.gif)

3) For the prefixes, a mid-function is used with upper case to take five characters from the company field to generate the prefixes

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/2.2%20-%20Prefix.gif)

### 3.3 - Prefix/Suffix Formatting Options
When inputting the prefix, dividers should not be added manually to each row. For example, “Company Alpha” should have its prefix input as “ALPHA” rather than “ALPHA\_”. The divider is instead set in the bottom left section of the options, should one be needed. It is also possible to set the formatting to suffixes instead. An example of the format of the outputted codes is also displayed in the user interface:

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/2.3%20-%20Prefix%20Format.gif)

For example, setting a prefix to ‘ALPHA’, maintaining prefix format, and setting the delimiter as ‘__’, will result in the output codes format of ‘ALPHA__1000’.

### 3.4 - Large Company Volumes
Generally, this converter is not designed for enormous volumes of unique companies due to user interface limitations. However, in instances where the number of companies are flagged as large (>150) a warning flag will be added to the user interface advising the use of automapping or importing files for correction individually, as this can cause further problems when performing corrections in other tabs.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/2.5%20-%20Prefix%20Limit.png)

### 3.5 - Saving Mappings
When all mappings have been filled out, pressing “Check & Save Mappings:” will either mark all fields in green if filled out correctly, or flag up an empty field. Adding prefixes is not mandatory for all companies, and will only flag up a warning, but remapping company names must be completed to flag this section as complete. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/2.4%20-%20Map%20Checks.gif)

When all mappings are confirmed, move to the ‘Description Settings’ tab.


#  <a name="desc"></a>4.0 – Description Settings:

### 4.1 - Selecting Description Corrections
Similar to the prefix tab, inconsistent descriptions do not have to be corrected, but generating a new COA is dependent on the completion of both the prefix tab as well as this section. Selecting yes enables the “Check Descriptions” Menu.

When checking for account codes with inconsistent descriptions, it is also possible to reduce the number of inconsistencies using the options. If there is a high volume of inconsistent descriptions, this can be corrected by trimming, as well as adjusting their formatting to lower or upper case since this is common formatting issue between tabs. Title case is not available due to the unpredictable impact of special characters on this function.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/3.0%20-%20Desc%20Manual.gif)

When ‘Check Descriptions’ is pressed, a list of account codes and their description options will be generated. If none are present, a notification will pop up prompting to move to the COA Regeneration tab. Otherwise, the list of inconsistent code descriptions will be shown.

### 4.2 - Automapping Descriptions
The Descriptions column contains a drop down of all possible mapping options for a specific code. If there is a significant volume of codes, it is possible to AutoMap the descriptions in priority order.

For example, if all codes in the CL (Closing) tab appear to be correct, whilst the PY (Prior Year) and OP (Opening) have clear spelling errors, then the AutoMap could be set to “CL > OP > PY” prioritisation order. This will automatically select all available descriptions in the Closing tab first, and if not present defer to the Opening tab, then the Prior tab.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/3.1-%20Desc%20Auto.gif)

Prioritisation order can also be set within an individual tab itself. By default, it is set to take the longest available string in a tab, but it is also possible to select first instance of a string if this is needed. Manual adjustments are also still possible after automapping if there is a specific exception to the rule.

When “Check & Save Mappings” is selected, it will automatically flag up blank description selections the same way as in the prefix settings tab. Otherwise, if all selections are made, move on to the COA Regeneration tab.

### 4.3 - Large Volume of Inconsistent Descriptions
Much like with prefixes, a large volume of descriptions (>300) will be flagged up. The interface for descriptions has been set to disable its canvas display, as large volumes usually indicates an entire tab of data has different descriptions to another tab. For TB files with thousands of lines this can easily overwhelm the user interface limits for widget generation.

However, whilst the canvas display is disabled, it is still possible to prioritise by tab for automapping. As such, the file will need to be manually reviewed to determine which tab should be prioritised. Auto-mapping and saving otherwise works as normal.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/3.2%20-%20Desc%20Limit.png)


#  <a name="coa"></a>5.0 – Chart of Accounts Generation:
### 5.1 - Pre-requisites to Generate a New COA
It is only possible to regenerate a chart of accounts if both the Prefix Settings and Description Settings Tabs have been completed. This is because the data must have had all errors relating to these tabs purged from the trial balance, or this section will regenerate the same errors in the COA and cause inconsistencies when loaded into a financial analyser.

### 5.2 - Selecting COA Mapping Sources
When generating a new COA, it is possible to isolate the potential mappings to just its sources files COA data. If this is selected, then it will likely result in a large number of unmapped codes if the original COA was incomplete but is useful for assuring data consistency of a specific companies’ mappings.

Setting “Extend mappings to all TBs” will first search for a code mapping in the source file as in the option above, but if not found, will defer to any other trial balance COA’s that were imported for an alternative mapping. This is particularly useful when all companies are known to use the same mappings across entities, but each files COA only contains codes with movement during the year.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/4.0%20-%20COA%20Source.gif)

### 5.3 - Non-standard COA Mappings
The TB .xlsm template has a limited number of standard COA mappings, with deviation resulting in potential errors when mappings to balance sheet or income statement on upload to the dashboard. When the COA is regenerated and mapped, it will check for any mappings that are not standard selections and add these to the user interface.

Approximate mapping is available to correct this should the volume be too excessive to do so manually. For example, if a trial balance includes an ‘A1 INTAN. ASSET’ mapping, it would infer from the left string that this should be mapped to ‘A1 – Intangible Assets’. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/4.1%20-%20COA%20Auto.gif)

Alternatively, these custom mappings can be maintained, and manual adjustments can be made after export where applicable.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/4.2%20-%20COA%20Checks.gif)

Once all non-standard codes are corrected and “Check & Save Mappings” is selected, move on to the Export Data tab.

### 5.4 - Excessive Non-standard COA Mappings
As with prefixes and descriptions, inconsistent COA mappings also have a GUI limit (<200) in place. Given that there is only a small volume of possible COA mappings, anything greater than this indicates that a client has not standardised their COA mappings. In these instances, none of the inconsistent mappings can be corrected as the current script is reliant on pulling directly from the canvas user interface selections.

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/4.3%20-%20COA%20Limit.png)

#  <a name="export"></a>6.0 – Export Data:

### 6.1 - Review Data
This tab will display the data input, adjustments made, and output for both the trial balance data and chart of accounts. If any sections have not been completed this will be flagged up accordingly.

1) Example of data where all corrections have been performed

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/5.0%20-%20Review.gif)

2) Example of data where descriptions have not been checked for duplicates, so a new COA has not been generated

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/5.1%20-%20Incomplete%20Review.png)

The data can be exported in several formats, including the following:

- Raw TB/COA – Exports the original unedited data (aside from filtering 0 values on import), but consolidated by each period tab.
- Adjusted TB/COA – Exports the edited data, including the prefixes, updated descriptions, and regenerated COA if available, consolidated by each period tab. It is also possible to remove all unmapped COA entries from the export.
- Detailed Meta TB/COA – Mainly used for assurance testing, exports a file including some hidden columns not normally present in regular exports, showing each stage of a column conversion to flag up any potential errors that occurred.

Select an export directory and export the file, which will be saved as ‘Trial Balance Export.xlsx’. Note that any file in the selected directory with this name will be overwritten. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/b8b31d343d18f8018609b37da280b9a90f6349d5/Readme%20Gifs%20&%20Images/6.0%20-%20Excel.gif)

The export template is saved in .xlsx format for simplicity, as exporting directly to the original .xlsm template would create an unnecessary dependency when the data can be directly copy/pasted manually.
