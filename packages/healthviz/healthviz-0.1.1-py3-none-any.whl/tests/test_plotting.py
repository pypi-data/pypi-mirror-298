import pandas as pd
from healthviz.visualization import Visualizer

# Sample data for testing
sample_data = pd.DataFrame({'heart_rate': [72, 75, 78, 120, 130, 200]})

# Create a Visualizer instance
visualizer = Visualizer(data=sample_data)

# Generate the plots
visualizer.plot_histogram('heart_rate')
visualizer.plot_scatter('heart_rate', 'heart_rate')  # Example for scatter
