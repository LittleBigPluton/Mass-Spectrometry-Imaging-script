# Import libraries
import visualization as vs
import pandas as pd
import io
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

file_path = "20191017_liver_4v_75um_Analyte_1AFAMM_1_pixel_intensities.csv"
raw_data = pd.read_csv(file_path,skiprows=[0,1],index_col=None)
raw_data = raw_data.drop(columns=['mol_formula','adduct','moleculeNames','moleculeIds'])
raw_data = raw_data.T
raw_data.columns = raw_data.iloc[0]
raw_data = raw_data.drop(['mz'])
# Extract mz values from the data
mz_values = list(raw_data.columns)

# Extract numbers and prepare for MultiIndex
extracted_numbers = raw_data.index.str.extractall('(\d+)')[0].unstack()
extracted_numbers.columns = ['X', 'Y']

# Convert to integers
extracted_numbers = extracted_numbers.astype(int)

# Create a MultiIndex from the DataFrame columns
multi_index = pd.MultiIndex.from_frame(extracted_numbers)

# Assign the MultiIndex to your original DataFrame
raw_data.index = multi_index
file_path = "cleaned_"+file_path
raw_data.to_csv(file_path)
raw_data = None

########################################
#####     Data Preprocessing       #####
########################################
#####       Example File 2         #####
########################################

file_path = "Sample_PL.txt"
# Read data from a tab-separated file and set up the DataFrame.
# Change delimiter to use other seperations
try:
    # Open file again to extract column names
    with open(file_path,'r') as file:
        lines = file.readlines()

    # Extract column names from the fourth line (index 3)
    # Split by tab and strip to remove any leading/trailing whitespace
    column_names = ["Index", "X", "Y"] + lines[3].strip().split('\t')

    # Use lines from the fifth line onwards (index 4) for data
    data_str = ''.join(lines[4:])

    # Convert the data string into a StringIO object
    # StringIO creates in-memory text stream from data_str
    # to give it to the DataFrame as a virtual file
    data_io = io.StringIO(data_str)

    # Read the data into a DataFrame
    raw_data = pd.read_csv(data_io, delimiter='\t', header=None)

    # Rename the columns in the DataFrame with the extracted column names
    raw_data.columns = column_names + list(raw_data.columns[-2:])
    # Print out first 10 rows of the data to have a sight
    print("First the rows of the data is: ")
    print(raw_data.head(10))
    print(f"Data includes {raw_data.shape[0]} rows and {raw_data.shape[1]} columns.")
    file_path = "cleaned_"+file_path
    raw_data.to_csv(file_path)


except FileNotFoundError as e:
    print("File not found. Please check the file path and try again.")
    print(e)
    exit()


########################################
#####       Data Processing        #####
########################################


# Set file path. If it is in the same folder with the script just file name is required
# Otherwise, full path is needed
file_path = "cleaned_Sample_PL.txt"
select_molecule = False
if select_molecule:
    # Print out whole observed molecules
    print(mz_values)
    # Set desired molecule
    molecule = str(input("Please select one molecule from the list to plot: "))
else:
    molecule = "766.5389"
# Create plotting object
plot = vs.visualize(file_path)
plot.create_data_frame()
# Give desired molecule
plot.set_molecule(molecule)
# Normalize the data by TIC
#plot.normalize_by_TIC()
# Plot normalized data using heatmap method
plot.plot_heatmap(show = True,save=True)
