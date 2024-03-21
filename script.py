#!/usr/bin/python3

###############################
#####   Import Libraries  #####
###############################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

###############################
##  Define Plotting Library  ##
###############################

import pandas as pd

class data_process:

    def __init__(self, file_path):
        ########################################################################
        # Parameter:                                                          ##
        # - file_path: Data file's name or complete path to read and use data ##
        # - data: Pandas DataFrame to manipulate easily                       ##
        # - column_names: To extract column names from the file               ##
        # - Xunique: To create a meshgrid for colormesh, unique x values      ##
        # - Yunique: To create a meshgrid for colormesh, unique y values      ##
        # - Molecule: Desired m/z value to visualize                          ##
        ########################################################################

        #Initialize with file path and empty data attributes.
        self.file_path = file_path
        self.data = None
        self.column_names = None
        self.Xunique = None
        self.Yunique = None
        self.molecule = None

    def create_data_frame(self):
        # Read data from a tab-separated file and set up the DataFrame.
        # Change delimiter to use other seperations
        try:
            # Open file again to extract column names
            with open(self.file_path,'r') as file:
                lines = file.readlines()

            # Extract column names from the fourth line (index 3)
            # Split by tab and strip to remove any leading/trailing whitespace
            self.column_names = ["Index", "X", "Y"] + lines[3].strip().split('\t')

            # Use lines from the fifth line onwards (index 4) for data
            data_str = ''.join(lines[4:])

            # Convert the data string into a StringIO object
            # StringIO creates in-memory text stream from data_str
            # to give it to the DataFrame as a virtual file
            data_io = io.StringIO(data_str)

            # Read the data into a DataFrame
            self.data = pd.read_csv(data_io, delimiter='\t', header=None)

            # Rename the columns in the DataFrame with the extracted column names
            self.data.columns = self.column_names + list(self.data.columns[-2:])
            # Print out first 10 rows of the data to have a sight
            print("First the rows of the data is: ")
            print(self.data.head(10))
            print(f"Data includes {self.data.shape[0]} rows and {self.data.shape[1]} columns.")

        except FileNotFoundError as e:
            print("File not found. Please check the file path and try again.")
            print(e)
            exit()

    def get_unique_coordinates(self):
        # Get unique values of XY coordinates
        self.Xunique = self.data['X'].unique()
        self.Yunique = self.data['Y'].unique()

    def get_column_names(self):
        print(self.data.columns)
        return self.data.columns

    def get_DataFrame(self):
        return self.data

    def set_molecule(self,molecule):
        self.molecule = str(molecule)

    def clean_data(self,drop_columns):
        # Drop columns are list include names of not desired columns
        # Make sure the list contains column names in the correct data type
        # like int, float, str and so on.
        try:
            self.data.drop(drop_columns, axis=1, inplace=True)
            print(f"Columns {drop_columns} were deleted from the DataFrame")
        except KeyError as e:
            print(f"Error removing columns: {e}")

    def normalize_by_TIC(self):
        # Calculate Total Ion Current (TIC) for normalization,
        # excluding 'Index', 'X', 'Y', and the last two unnecessary columns.
        # self.column_names includes only Index, X, Y and rest of the columns
        # except last two not necessary columns
        self.data["TIC"] = self.data[self.column_names[3:]].sum(axis=1)
        # To normalize all data, uncomment the following code but computation time is longer
        # self.data[self.column_names[3:]]=self.data[self.column_names[3:]].div(self.data["TIC"], axis=0)
        self.data[self.molecule] = self.data[self.molecule].div(self.data["TIC"], axis = 0)

class visualize(data_process):
    def save_plot(self,figure, type, directory = '.',format = 'png', dpi = 300):
        ####################################################################################################
        # Parameters:                                                                                     ##
        # - figure: The matplotlib figure to save.                                                        ##
        # - savepath: Name of the file to save the figure as.                                             ##
        # - directory: The directory where the figure should be saved. Defaults to the current directory. ##
        # - format: The file format (e.g., 'png', 'jpg', 'pdf', 'svg'). Defaults to 'png'.                ##
        # - dpi: The resolution in dots per inch. Defaults to 300 for high quality.                       ##
        ####################################################################################################
        # Extract sample name from the data file's path
        sample_name = self.file_path[:-4]
        save_path = str(f"{sample_name}_{self.molecule}_{type}.{format}")

        # Save the figure
        figure.savefig(save_path, format=format, dpi=dpi)
        print(f"Plot saved as '{save_path}'.")

    def plot_meshgrid(self,figure_size = (10,8), show = False, save = False):
        # Get unique coordinates to create meshgrid
        self.get_unique_coordinates()
        # Create a meshgrid using unique x and y values
        X, Y = np.meshgrid(self.Xunique, self.Yunique)
        # Normalize intensities
        intensity = self.data[self.molecule]
        # Reshape intensty column of the molecule to create colormesh
        intensity = intensity.to_numpy().reshape(len(self.Yunique), len(self.Xunique))

        # Create a meshgrid plot
        fig,ax = plt.subplots(figsize = figure_size)
        c = ax.pcolormesh(X, Y, intensity, cmap ="CMRmap" , shading='auto')
        # Create colorbar
        fig.colorbar(c, ax=ax, label='Intensity')
        # Create colormesh and inverse the Y-axis to get correct structure
        plt.gca().invert_yaxis()
        # Set title and axis names
        ax.set_title(f"Colormesh of Molecule {self.molecule}")
        ax.set_xlabel("X coordinates on the plane")
        ax.set_ylabel("Y coordinates on the plane")
        if show:
            plt.show()
        if save:
            self.save_plot(fig, "colormesh")


    def plot_heatmap(self, figure_size = (10,8), show = False, save = False):
        # Create the pivot table to plot data as a heatmap
        pivot_table = self.data.pivot("Y", "X", self.molecule)
        # Create the intensity heatmap
        fig, ax = plt.subplots(figsize=figure_size)
        # Display the heatmap
        heatmap = ax.imshow(pivot_table,origin ='upper',cmap="CMRmap",interpolation='nearest')
        # Create the colorbar and set its label
        fig.colorbar(heatmap, ax=ax, label='Intensity')
        # Set title and axis names
        ax.set_title(f'Heatmap of Molecule {molecule} Density')
        ax.set_xlabel("X coordinates on the plane")
        ax.set_ylabel("Y coordinates on the plane")
        if show:
            plt.show()
        if save:
            self.save_plot(fig, "heatmap")



# Set file path. If it is in the same folder with the script justfile name is required
# Otherwise, full path is needed
file_path = "example.txt"
# Set desired molecule
molecule = "123.456"
# Create plotting object
plot = visualize(file_path)
plot.create_data_frame()
#columns = plot.get_column_names()
#plot.clean_data(columns[-2:])
# Give desired molecule
plot.set_molecule(molecule)
# Normalize the data by TIC
plot.normalize_by_TIC()
# Plot normalized data using colormesh method
plot.plot_meshgrid(show = True,save=True)
# Plot normalized data using heatmap method
plot.plot_heatmap(show = True,save=True)
