import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

class DigitalTwin:
    def __init__(self, model):
        self.model = model
        self.sensor_data = None
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(children=[
            html.H1(children='Digital Twin Simulation'),
            dcc.Graph(id='simulation-graph'),
            dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
        ])
        self.app.callback(
            Output('simulation-graph', 'figure'),
            [Input('interval-component', 'n_intervals')]
        )(self.update_graph)

    def load_sensor_data(self, data):
        self.sensor_data = data

    def run_simulation(self):
        if self.sensor_data is None:
            raise ValueError("Sensor data not loaded")
        simulated_data = self.sensor_data * np.random.normal(1, 0.05, self.sensor_data.shape)
        return simulated_data

    def update_graph(self, n_intervals):
        simulated_data = self.run_simulation()
        figure = {
            'data': [
                {'x': simulated_data[:, 0], 'y': simulated_data[:, 1], 'type': 'line', 'name': 'Simulation'}
            ],
            'layout': {
                'title': 'Digital Twin Simulation Results'
            }
        }
        return figure

    def visualize_results(self):
        self.app.run_server(debug=True)

# Example usage
if __name__ == "__main__":
    model = np.zeros((100, 3))
    dt = DigitalTwin(model)
    sensor_data = np.random.rand(100, 3)
    dt.load_sensor_data(sensor_data)
    dt.visualize_results()
