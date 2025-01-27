import random
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

class MonitoringTools:
    def __init__(self):
        self.telemetry_data = []
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(children=[
            html.H1(children='Telemetry Data Visualization'),
            dcc.Graph(id='telemetry-graph'),
            dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
        ])
        self.app.callback(
            Output('telemetry-graph', 'figure'),
            [Input('interval-component', 'n_intervals')]
        )(self.update_graph)

    def collect_telemetry(self, source):
        data = {
            'source': source,
            'timestamp': time.time(),
            'value': random.uniform(0, 100)
        }
        self.telemetry_data.append(data)
        print(f"Collected data from {source}: {data['value']} at {data['timestamp']}")

    def aggregate_telemetry(self):
        aggregated_data = {}
        for data in self.telemetry_data:
            source = data['source']
            if source not in aggregated_data:
                aggregated_data[source] = []
            aggregated_data[source].append(data['value'])
        return aggregated_data

    def update_graph(self, n_intervals):
        aggregated_data = self.aggregate_telemetry()
        figure = {
            'data': [
                {'x': list(range(len(values))), 'y': values, 'type': 'line', 'name': source}
                for source, values in aggregated_data.items()
            ],
            'layout': {
                'title': 'Telemetry Data Visualization'
            }
        }
        return figure

    def visualize_telemetry(self, aggregated_data):
        self.app.run_server(debug=True)

    def generate_alerts(self, aggregated_data, threshold=80):
        alerts = []
        for source, values in aggregated_data.items():
            for value in values:
                if value > threshold:
                    alert = f"Alert! {source} value {value} exceeds threshold {threshold}"
                    alerts.append(alert)
                    print(alert)
        return alerts

# Example usage
if __name__ == "__main__":
    mt = MonitoringTools()

    # Simulate sensor data collection
    for _ in range(10):
        mt.collect_telemetry("Aircraft")
        mt.collect_telemetry("Weather Station")
        mt.collect_telemetry("Ground Sensor")
        time.sleep(1)

    # Process and analyze data
    aggregated_data = mt.aggregate_telemetry()

    # Visualize data using dashboards
    mt.visualize_telemetry(aggregated_data)

    # Generate alerts
    mt.generate_alerts(aggregated_data)
