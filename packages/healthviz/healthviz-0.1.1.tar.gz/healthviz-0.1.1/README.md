# HealthViz

HealthViz is a Python package designed for visualizing and analyzing health data. It provides functionalities to detect anomalies and generate various visualizations, including histograms and scatter plots, making it an essential tool for health data analysis.

## Features

- **Anomaly Detection**: Identify anomalies in health-related data, such as heart rate and other vital signs.
- **Easy-to-Use Visualizations**: Generate insightful visualizations, including:
  - **Histograms**: For understanding the distribution of health metrics.
  - **Scatter Plots**: For exploring relationships between different health variables.

## Installation

You can install HealthViz using pip:

```bash
pip install healthviz
```

## Usage

To get started with HealthViz, follow the example below:

```python
import pandas as pd
from healthviz.visualization import Visualizer

# Sample data
data = pd.DataFrame({'heart_rate': [72, 80, 200, 100]})

# Initialize the Visualizer
visualizer = Visualizer(data)

# Create a histogram of heart rate data
visualizer.plot_histogram('heart_rate')
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report issues, please open an issue or submit a pull request on the [GitHub repository](https://github.com/Saunakghosh10/health-viz).

## License

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgements

- This package leverages popular libraries such as `pandas` and `matplotlib` for data manipulation and visualization.
- Special thanks to the community for their continuous support and contributions.
