import random
import time
import matplotlib.pyplot as plt

class EnvironmentalMonitoring:
    def __init__(self):
        self.sensor_data = []

    def collect_sensor_data(self, sensor_type):
        data = {
            'sensor_type': sensor_type,
            'timestamp': time.time(),
            'value': random.uniform(0, 100)
        }
        self.sensor_data.append(data)
        print(f"Collected data from {sensor_type}: {data['value']} at {data['timestamp']}")

    def analyze_trends(self):
        trends = {}
        for data in self.sensor_data:
            sensor_type = data['sensor_type']
            if sensor_type not in trends:
                trends[sensor_type] = []
            trends[sensor_type].append(data['value'])
        return trends

    def generate_alerts(self, trends, threshold=80):
        alerts = []
        for sensor_type, values in trends.items():
            for value in values:
                if value > threshold:
                    alert = f"Alert! {sensor_type} value {value} exceeds threshold {threshold}"
                    alerts.append(alert)
                    print(alert)
        return alerts

    def visualize_data(self, trends):
        for sensor_type, values in trends.items():
            plt.plot(values, label=sensor_type)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Environmental Sensor Data Visualization')
        plt.legend()
        plt.show()

# Example usage
if __name__ == "__main__":
    em = EnvironmentalMonitoring()

    # Simulate sensor data collection
    for _ in range(10):
        em.collect_sensor_data("Air Quality")
        em.collect_sensor_data("Water Quality")
        time.sleep(1)

    # Analyze trends and anomalies
    trends = em.analyze_trends()

    # Generate alerts
    em.generate_alerts(trends)

    # Visualize data
    em.visualize_data(trends)
