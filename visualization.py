###############################
#####   Import Libraries  #####
###############################
import matplotlib.pyplot as plt
import numpy as np
# Import data processing library in order to build on top
import processing as pr

####################################
##  Define Visualization Library  ##
####################################

class visualize(pr.data_process):
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
        ax.set_title(f'Heatmap of Molecule {self.molecule} Density')
        ax.set_xlabel("X coordinates on the plane")
        ax.set_ylabel("Y coordinates on the plane")
        if show:
            plt.show()
        if save:
            self.save_plot(fig, "heatmap")
