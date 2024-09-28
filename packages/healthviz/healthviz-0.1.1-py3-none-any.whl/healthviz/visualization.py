
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self, data):
        self.data = data

    def line_chart(self, x_column, y_column, title=None):
        """Create a line chart for the specified x and y columns."""
        fig = go.Figure(data=go.Scatter(x=self.data[x_column], y=self.data[y_column], mode='lines'))
        if title:
            fig.update_layout(title=title)
        return fig

    def bar_chart(self, x_column, y_column, title=None):
        """Create a bar chart for the specified x and y columns."""
        fig = go.Figure(data=go.Bar(x=self.data[x_column], y=self.data[y_column]))
        if title:
            fig.update_layout(title=title)
        return fig

    def scatter_plot(self, x_column, y_column, title=None):
        """Create a scatter plot for the specified x and y columns."""
        fig = go.Figure(data=go.Scatter(x=self.data[x_column], y=self.data[y_column], mode='markers'))
        if title:
            fig.update_layout(title=title)
        return fig
    
    def plot_histogram(self, column):
        """Plot histogram of the specified column."""
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[column], bins=30, kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

    def plot_scatter(self, column1, column2):
        """Plot scatter plot between two columns."""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.data[column1], y=self.data[column2])
        plt.title(f'Scatter Plot between {column1} and {column2}')
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.show()