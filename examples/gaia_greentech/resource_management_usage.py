import random
import time
import matplotlib.pyplot as plt

class ResourceManagement:
    def __init__(self):
        self.resource_data = []

    def track_resource_usage(self, resource_type):
        data = {
            'resource_type': resource_type,
            'timestamp': time.time(),
            'usage': random.uniform(0, 100)
        }
        self.resource_data.append(data)
        print(f"Tracked usage for {resource_type}: {data['usage']} at {data['timestamp']}")

    def identify_waste_areas(self):
        waste_areas = {}
        for data in self.resource_data:
            resource_type = data['resource_type']
            if resource_type not in waste_areas:
                waste_areas[resource_type] = []
            waste_areas[resource_type].append(data['usage'])
        return waste_areas

    def implement_reduction_measures(self, waste_areas, threshold=50):
        reduction_measures = []
        for resource_type, usages in waste_areas.items():
            for usage in usages:
                if usage > threshold:
                    measure = f"Implement reduction for {resource_type} usage {usage} exceeding threshold {threshold}"
                    reduction_measures.append(measure)
                    print(measure)
        return reduction_measures

    def optimize_allocation(self, waste_areas):
        optimized_allocation = {}
        for resource_type, usages in waste_areas.items():
            optimized_allocation[resource_type] = sum(usages) / len(usages)
        return optimized_allocation

    def visualize_data(self, waste_areas):
        for resource_type, usages in waste_areas.items():
            plt.plot(usages, label=resource_type)
        plt.xlabel('Time')
        plt.ylabel('Usage')
        plt.title('Resource Usage Visualization')
        plt.legend()
        plt.show()

# Example usage
if __name__ == "__main__":
    rm = ResourceManagement()

    # Simulate resource usage tracking
    for _ in range(10):
        rm.track_resource_usage("Water")
        rm.track_resource_usage("Raw Materials")
        time.sleep(1)

    # Identify waste areas
    waste_areas = rm.identify_waste_areas()

    # Implement reduction measures
    rm.implement_reduction_measures(waste_areas)

    # Optimize resource allocation
    optimized_allocation = rm.optimize_allocation(waste_areas)
    print("Optimized Allocation:", optimized_allocation)

    # Visualize data
    rm.visualize_data(waste_areas)
