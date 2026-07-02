# Import libraries
import pandas as pd
import io

from msi_visualization.visualization import visualize
from config import (
    raw_data_dir,
    processed_data_dir
)
#######################################
### The following cleaning process can
### be skipped if the data is in the
##  following form:
### X   |   Y | 123.456 | 255.233 | ...
### 0.1 | 0.1 | 0.9     | 0.3     | ...
### 0.1 | 0.2 | 0.3     | 0.4     | ...
### ... | ... | ...     | ...     | ...
########################################

########################################
#####     Data Preprocessing       #####
########################################
#####       Example File 1         #####
########################################

# Clean the data and get rid of unnecessary columns/rows and shape the data

sample_data_1_name = "20191017_liver_4v_75um_Analyte_1AFAMM_1_pixel_intensities.csv"
sample_data_1_select_molecule = False
if sample_data_1_select_molecule:
    # Print out whole observed molecules
    print(mz_values)
    # Set desired molecule
    sample_data_1_molecule_mz = str(input("Please select one molecule from the list to plot: "))
else:
    sample_data_1_molecule_mz = "279.232953829"

msi_feature_data = raw_data_dir / sample_data_1_name
sample_data_1 = visualize(msi_feature_data)
sample_data_1.clean_transposed_msi_feature_table(processed_data_dir, sample_data_1_name)
# Create plotting object
sample_data_1.create_data_frame()
# Give desired molecule
sample_data_1.set_molecule(sample_data_1_molecule_mz)
# Plot normalized data using heatmap method
sample_data_1.plot_heatmap(sample_data_1_molecule_mz, show = True,save=True)

########################################
#####     Data Preprocessing       #####
########################################
#####       Example File 2         #####
########################################

tab_separated_data_name = "Sample_PL.txt"
sample_data_2_select_molecule = False
sample_data_2_TIC = True
if sample_data_2_select_molecule:
    # Print out whole observed molecules
    print(mz_values)
    # Set desired molecule
    sample_data_2_molecule_mz = str(input("Please select one molecule from the list to plot: "))
else:
    sample_data_2_molecule_mz = "766.5389"

tab_seperated_data = raw_data_dir / tab_separated_data_name
# Create plotting object
sample_data_2 = visualize(tab_seperated_data)
sample_data_2.clean_tab_separated_msi_export(processed_data_dir,tab_separated_data_name)
sample_data_2.create_data_frame()
# Give desired molecule
sample_data_2.set_molecule(sample_data_2_molecule_mz)
# Normalize the data by TIC
sample_data_2.normalize_by_TIC(all=sample_data_2_TIC)
# Plot normalized data using heatmap method
sample_data_2.plot_heatmap(sample_data_2_molecule_mz, TIC = sample_data_2_TIC, show = True,save=True)
