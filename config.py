from pathlib import Path

root_directory = Path(__file__).resolve().parent

# Data folder
data_dir = root_directory / "data"
raw_data_dir = data_dir / "raw"
processed_data_dir = data_dir / "processed"

# Figure folder
figures_dir = root_directory / "figures"

# Create directories if they do not already exist
data_dir.mkdir(parents=True, exist_ok=True)
raw_data_dir.mkdir(parents=True, exist_ok=True)
processed_data_dir.mkdir(parents=True, exist_ok=True)
figures_dir.mkdir(parents=True, exist_ok=True)

# Figure parameters
figure_format = "png"
dpi_resolution = 300
heat_map_size = (10,8)
