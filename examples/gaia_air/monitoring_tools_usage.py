import random
import time
import matplotlib.pyplot as plt

class MonitoringTools:
    def __init__(self):
        self.telemetry_data = []

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

    def visualize_telemetry(self, aggregated_data):
        for source, values in aggregated_data.items():
            plt.plot(values, label=source)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Telemetry Data Visualization')
        plt.legend()
        plt.show()

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
