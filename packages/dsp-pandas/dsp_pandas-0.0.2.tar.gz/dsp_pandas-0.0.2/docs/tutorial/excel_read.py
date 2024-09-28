# %% [markdown]
# # Read all sheets from an Excel file
# Example data with 83 individuals.

# %%
from dsp_pandas.io import read_all_excel_sheets

fname = "ProteomicsData_DIA_demo.xlsx"

excel_sheets = read_all_excel_sheets(fname)
excel_sheets.sheet_names

# %% [markdown]
# Then each sheet is available as a DataFrame via an attribute with the same name as the sheet.
# (White spaces are replaced by underscores.)

# %%
excel_sheets.Proteomics.filter(like="MS2Quantity")

# %% [markdown]
# The analytical sample id is used in the columns of the above Proteomics data (MS2 Quantification).


# %%
excel_sheets.Design

# %% [markdown]
# The `Design` sheet contains the mapping of the analytical sample id to the biological sample id
# used in the (artifical) clinical data:

# %%
excel_sheets.Clinic

# %%
