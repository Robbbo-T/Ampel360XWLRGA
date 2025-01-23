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

    def monitor_qps_components(self, qps_components):
        for component in qps_components:
            self.collect_telemetry(component)
        aggregated_data = self.aggregate_telemetry()
        self.visualize_telemetry(aggregated_data)
        self.generate_alerts(aggregated_data)

    def collect_qps_telemetry(self, component_id):
        # Simulate data collection from a QPS component
        data = {
            'temperature': [75, 76, 77, 78, 79],
            'vibration': [0.02, 0.03, 0.04, 0.05, 0.06],
            'pressure': [101, 102, 103, 104, 105]
        }
        return data

    def visualize_qps_telemetry(self, qps_data):
        for metric, values in qps_data.items():
            plt.plot(values, label=metric)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('QPS Telemetry Data Visualization')
        plt.legend()
        plt.show()

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

    # Monitor QPS components
    qps_components = ["QPS-CMP-001", "QPS-CMP-002", "QPS-CMP-003"]
    mt.monitor_qps_components(qps_components)

    # Collect and visualize QPS telemetry data
    qps_data = mt.collect_qps_telemetry("QPS-CMP-001")
    mt.visualize_qps_telemetry(qps_data)
