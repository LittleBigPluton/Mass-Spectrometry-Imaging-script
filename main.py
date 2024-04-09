# Import libraries
import visualization as vs

# Set file path. If it is in the same folder with the script justfile name is required
# Otherwise, full path is needed
file_path = "example.txt"
# Set desired molecule
molecule = "123.456"
# Create plotting object
plot = vs.visualize(file_path)
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
