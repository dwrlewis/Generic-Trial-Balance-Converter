# Trial Balance Converter Readme
# Contents
[1.0 – Overview](#overview)

[2.0 – Import Selection](#import)

[3.0 – Prefix Settings](#prefix)

[4.0 – Description Settings](#desc)

[5.0 – Chart of Accounts Generation](#coa)

[6.0 – Export Data](#export)


# <a name="overview"></a>1.0 – Overview:

## Preface
This program is designed for the checking & correction of financial trial balance data in .xlsm templates. These templates are filled out externally by clients from trial balance data exports, and often contain discrepancies that results in errors aligning the trial balance with its corresponding journal data when loaded into a financial analyser dashboard. This program is designed to thoroughly check through data at all stages, including: 

- Preliminary checks for missing key data, missing secondary data, and value fields containing non-numeric entries
- Standardisation of company naming syntax and prefix/suffixing of account codes
- Correction of inconsistent descriptions for the same account code
- Generation of an updated chart of account without duplicates or inconsistencies
- Remapping of chart of accounts in instances where non-standard mappings are present
- Export of the data, consolidated into one file if multiple .xlsm files were input

Note: The .xlsm files saved here have had all company specific info such as macros and superfluous tabs removed. The program has not been changed to accommodate for this, as both the dummy .xlsm files and original templates can be run without adjustment.

## Interpreter Settings
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
## File Path & Import
The converter can be used for checking and correction of an individual .xlsm template or multiple simultaneously, the latter of which will result in all data being consolidated into a single file for export.

The User Interface opens in the Import Selection tab. Select the import directory in the top left of this tab, which will automatically display a list of .xlsm files in the selected path.

The data to import can be selected down to the individual tabs. For example, one file may have its Prior, Closing and COA imported, whilst another may only have a Closing imported. 

![alt text](https://github.com/dwrlewis/Trial-Balance-Converter/blob/122afb7b9c98e57406c37bdbac849a3f104898aa/Readme%20Gifs/1%20-%20Tab%20Selection.gif)

The header columns are also selectable buttons to enable/disable the import for an entire tab set, as are the Filenames which enable/disables the import for that particular file.

The Filter Null Amounts option is designed for unusually large system exports containing every possible code in a system, even ones that have seen no movement. As such, this can be used to remove all irrelevant trial balance lines for each period, reducing both load time and redundant error flags.

Once selections are made, Load Trial Balances can be selected in the bottom left.
## Import Results and Error Flags
Once all the files in the selected folder have been checked, the user interface colours will update to display any immediate errors it may have flagged in a specific tab of a dataset:

- Green highlights mean that there were no errors found in the data tab.
- Yellow highlights mean there are minor errors present. This can include things like null descriptions or amount fields where zeroes may have been left as null entries.
- Red highlights mean this tab of data could not be imported. This can be a result of missing company or account codes in their respective fields, non-numeric data in the amount field, or miscellaneous import errors such as missing tabs or column headers.

Hovering over a particular cell containing an error will display a list of all the errors that were found whilst try to import the data from that particular tab. It is also possible to change selections press Load Trial Balances again, if for example, you decide a particular dataset can be left out entirely based on errors flagged in a particular tab. 

Once the data imported data has been deemed adequate, move to the Prefix Settings tab of the user interface.

[INSERT IMAGE]


# <a name="prefix"></a>3.0 – Prefix Settings:
## Selecting Company & Prefix Corrections
The prefix settings tab is the first set of corrections to make to a trial balance. In the top left of this tab, there is a selection for this option. Note that whilst it is not mandatory to perform these checks, not doing so will disable any Description Settings that can be made in the next tab.

Once the selection is made, it will generate a list of all unique company names found across all imported data files in the interface. This is intended to flag inconsistencies in how companies have been entered across different tabs and files. For example, “Alpha Company Limited” might be entered as “Alpha Ltd” in a different tab of data, which would cause alignment errors when loaded into a financial analyser dashboard.

[INSERT IMAGE]

The user interface here effectively serves the same role as an excel style mapping document. The ‘New Comp. Mappings’ field is what the companies will be renamed as in the export, whilst the ‘Prefix/Suffix’ field will be added to all account codes for that respective company.

New mappings can be entered manually the same as in an excel, but it is also possible to automatically map data using the options on the left of the user interface. This is a more viable alternative for large numbers of companies.
## Additional Options
Both the ‘New Comp. Mappings’ and ‘Prefix/Suffix’ headers can be selected the same way as column selection in excel, which turns the border green and allows options adjustments to be applied.

By default, the Automap Column(s) function is set to use the whole string but can also be adjusted to draw from the left, mid, or right of the Imported Company field in the same way as excel. 

There are also casing adjustments for Upper, Lower, and Title, as well as trimming whitespace from the field, and a replace function that can be limited by casings.
## Prefix/Suffix Formatting Options
When inputting the prefix, dividers should not be added here. For example, ‘Company Alpha’ should have its prefix input as ‘ALPHA’ rather than ‘ALPHA\_’. The divider is instead set in the bottom left section of the options, should one be needed. It is also possible to set the formatting to suffixes instead. An example of the format of the outputted codes is also displayed here.

[INSERT IMAGE]
## Saving Mappings
When all mappings have been filled out, pressing ‘Check & Save Mappings:’ will either mark all fields in green if filled out correctly, or flag up an empty field. Adding prefixes is not mandatory, and will only flag up a warning, but remapping companies must be completed to flag this section as complete. 

When all mappings are confirmed, move to the ‘Description Settings’ tab.


#  <a name="desc"></a>4.0 – Description Settings:
## Selecting Company & Prefix Corrections
Similarly, to the prefixes tab, inconsistent descriptions do not have to be corrected, but this tab is dependent on the completion of the prefix settings tab. Selecting yes enable the Check Descriptions Menu.

When checking for account codes with inconsistent descriptions, it is possible to reduce the number of inconsistencies by trimming descriptions, as well as adjusting their formatting to lower or upper case. Title case is not available due to the impact of special characters on this function.

[INSERT IMAGE]

When ‘Check Descriptions’ is pressed, a list of account codes and their description options will be generated. If none or present, a notification will pop up prompting to move to the COA Regeneration tab. Otherwise, the number of inconsistent code descriptions will be shown.
## Automapping Descriptions
The Descriptions column contains a drop down containing all of the possible mapping options for a specific code. If there is a significant volume of codes, it is possible to AutoMap the descriptions in priority order.

[INSERT IMAGE]

For example, if all codes in the CL (Closing) tab appear to be correct, whilst the PY (Prior Year) and OP (Opening) have clear spelling errors, then the AutoMap could be set to ‘CL > OP > PY’ prioritisation order. This will automatically select all available descriptions in the Closing tab first, and if not present defer to the Opening tab, then the Prior tab.

Prioritisation order can also be set within an individual tab itself. By default, it is set to take the longest available string in a tab, but it is also possible to select first instance of a string if this is needed. Manual adjustments are also still possible after automapping.

When ‘Check & Save Mappings’ is selected, it will automatically flag up blank description selections the same way as in the prefix settings tab. Otherwise, if all selections are made, move on to the COA Regeneration tab.


#  <a name="coa"></a>5.0 – Chart of Accounts Generation:
## Pre-requisites to Generate a New COA
It is only possible to regenerate a chart of accounts if both the Prefix Settings and Description Settings Tabs have both been completed. This is because the data must have had all errors relating to these tabs purged from the trial balance, or this section would regenerate the same errors in the COA and cause inconsistencies when loaded into a financial analyser.
## Selecting Mapping Sources
When generating a new COA, it is possible to isolate the potential financial analyser mappings to just its sources files COA data. If this is selected, then it will likely result in a large number of unmapped codes if the original COA was incomplete but is useful in for assuring data consistency for a specific companies’ mappings.

Setting ‘Extend mappings to all TBs’ will first search for a code mapping in the source file, and if not found, defer to any other trial balance COA’s that were imported for an alternative mapping. This is particularly useful when all companies are known to use the same mappings across entities, but each files COA was only partially completed.

[INSERT IMAGE]
## Non-standard Mappings
The original .xlsm template had a limited number of mapping selections to draw from, with deviation of any kind resulting in errors on upload to the financial analyser. When the COA is regenerated and mapped, it will check for any mappings that are not present in the standard selections and add these to the user interface. 

Approximate mapping is available to correct this should the volume be too excessive to do so manually. For example, if a trial balance include an ‘A1 INTAN. ASSET’ mapping, it would infer from the left string that this should be mapped to ‘A1 – Intangible Assets’. 

Alternatively, these custom mappings can be maintained, as it was possible to add to the standard mappings field in the original .xlsm template for exceptional circumstances.

Once all non-standard codes are corrected and ‘Check & Save Mappings’ is selected, move on to the Export Data tab.


#  <a name="export"></a>6.0 – Export Data:
## Review Data
This tab will display the data input, adjustments made, and output for both the trial balance data and chart of accounts. If any sections have not been completed this will be flagged up accordingly.

The data can be exported in several formats, including the following:

- Raw TB/COA – Exports the original unedited data (aside from filtering 0 values on import), but consolidated by each period tab.
- Adjusted TB/COA – Exports the edited data, including the prefixes, updated descriptions, and regenerated COA if available, consolidated by each period tab.
- Detailed Meta TB/COA – Mainly used for assurance testing, exports a file including the hidden columns not normally present in regular exports, showing each stage of a column conversion to flag up any potential errors that occurred.

Select an export directory and export the file, which will be saved as ‘Trial Balance Export.xlsx’. Note that any file in the selected directory with this name will be overwritten. 

[INSERT IMAGE]

The export template is saved in .xlsx format for simplicity, as export to .xlsm was considered redundant since it created a dependency on the company template, and the data would normally be manually verified anyway. As such, it would be expected that the .xlsx export simply be copy/pasted into a new .xlsm template after data checks were performed.
