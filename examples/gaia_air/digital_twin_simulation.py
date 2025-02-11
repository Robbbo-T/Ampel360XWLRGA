import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt

class DigitalTwin:
    def __init__(self, model):
        """
        model: Initial model or reference data for the Digital Twin.
        """
        self.model = model  # Not heavily used in this example, but placeholder for a more sophisticated model.
        self.sensor_data = None
        self.flagged_data = []
        
        self.app = dash.Dash(__name__)
        
        # Layout with two graphs: one for simulation, one for flagged anomalies
        self.app.layout = html.Div(children=[
            html.H1(children='Digital Twin Simulation with Real-Time Analytics'),
            
            dcc.Graph(id='simulation-graph'),
            dcc.Graph(id='flagged-graph', style={'marginTop': '50px'}),

            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # 1000 ms = 1 second
                n_intervals=0
            )
        ])
        
        # Main callback for simulation and analytics
        self.app.callback(
            [Output('simulation-graph', 'figure'),
             Output('flagged-graph', 'figure')],
            [Input('interval-component', 'n_intervals')]
        )(self.update_graphs)

    def load_sensor_data(self, data):
        """
        Load or update sensor data that will be used for simulation.
        """
        self.sensor_data = data

    def sync_data(self, new_data):
        """
        Demonstrates automated data module synchronization.
        External modules can push new_data here to update the twin.
        """
        if self.sensor_data is None:
            self.sensor_data = new_data
        else:
            # Append or combine data. In a real scenario, we might store historical series
            self.sensor_data = np.vstack([self.sensor_data, new_data])

    def simulate_data(self):
        """
        Perform a simple simulation on top of the sensor data.
        Here, we randomly perturb the sensor data to mimic some real-time variation.
        """
        if self.sensor_data is None:
            raise ValueError("Sensor data not loaded")

        # Simple simulation: multiply by a small random factor
        simulated_data = self.sensor_data * np.random.normal(1, 0.05, self.sensor_data.shape)
        return simulated_data

    def analyze_data(self, simulated_data):
        """
        Example real-time analytics method to detect correlations or anomalies.
        We check pairwise correlations; if above a threshold, we flag the data.
        """
        # If your data is NxM, you can compute correlations among columns
        # For simplicity, assume last dimension are the features
        threshold = 0.8  # correlation threshold for flagging
        correlation_matrix = np.corrcoef(simulated_data.T)

        # Identify any correlation above the threshold
        flagged_indices = np.where(np.abs(correlation_matrix) > threshold)
        flagged_pairs = [(i, j) for i, j in zip(*flagged_indices) if i < j]  # avoid duplicates i-j, j-i

        flagged_info = {
            'correlation_matrix': correlation_matrix.tolist(),
            'flagged_pairs': flagged_pairs
        }

        # If flagged, store in self.flagged_data for display
        if flagged_pairs:
            self.flagged_data.append(flagged_info)

        return flagged_info

    def hierarchical_clustering(self, data, method='ward'):
        Z = linkage(data, method=method)
        return Z

    def plot_dendrogram(self, Z):
        plt.figure(figsize=(10, 7))
        plt.title("Dendrogram")
        dendrogram(Z)
        plt.show()

    def update_graphs(self, n_intervals):
        """
        Called every interval to:
        1) Simulate data
        2) Analyze for correlations
        3) Update the main simulation graph
        4) Update the flagged graph
        """
        simulated_data = self.simulate_data()
        flagged_info = self.analyze_data(simulated_data)

        # Perform hierarchical clustering
        Z = self.hierarchical_clustering(simulated_data)

        # Prepare the main simulation figure
        # For demonstration, plot the first two columns of the simulated data
        figure_simulation = {
            'data': [
                {
                    'x': np.arange(len(simulated_data)),
                    'y': simulated_data[:, 0],
                    'type': 'line',
                    'name': 'Feature 0'
                },
                {
                    'x': np.arange(len(simulated_data)),
                    'y': simulated_data[:, 1],
                    'type': 'line',
                    'name': 'Feature 1'
                }
            ],
            'layout': {'title': 'Real-Time Simulation'}
        }

        # Prepare the flagged anomalies figure:
        # Let's simply visualize how many flagged pairs we have accumulated over time.
        flagged_counts = [len(item['flagged_pairs']) for item in self.flagged_data]
        figure_flagged = {
            'data': [
                {
                    'x': list(range(len(flagged_counts))),
                    'y': flagged_counts,
                    'type': 'bar',
                    'name': 'Flagged Correlations'
                }
            ],
            'layout': {'title': 'Flagged Correlation Events Over Time'}
        }

        # Plot dendrogram
        self.plot_dendrogram(Z)

        return figure_simulation, figure_flagged

    def visualize_results(self):
        """
        Launch the Dash server. 
        """
        self.app.run_server(debug=True)


# Example usage
if __name__ == "__main__":
    # Initialize a placeholder model
    model = np.zeros((100, 3))

    dt = DigitalTwin(model)

    # Generate random initial sensor data
    sensor_data = np.random.rand(100, 3)
    dt.load_sensor_data(sensor_data)

    # In a real application, additional modules could periodically call dt.sync_data(new_data)
    # to push fresh sensor readings or updates.

    dt.visualize_results()
