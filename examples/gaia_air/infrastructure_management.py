import json
import time
from datetime import datetime

class InfrastructureManagement:
    def __init__(self):
        self.air_traffic_control = {}
        self.airport_facilities = {}
        self.ground_support_systems = {}

    def monitor_component(self, component_id, status):
        timestamp = datetime.now().isoformat()
        log_entry = {
            "component_id": component_id,
            "status": status,
            "timestamp": timestamp
        }
        print(f"Monitoring component {component_id}: {status} at {timestamp}")
        return log_entry

    def optimize_resource_allocation(self, resources):
        optimized_resources = sorted(resources, key=lambda x: x['priority'], reverse=True)
        print("Optimized resource allocation:", optimized_resources)
        return optimized_resources

    def automate_scheduling(self, tasks):
        scheduled_tasks = sorted(tasks, key=lambda x: x['deadline'])
        print("Automated scheduling of tasks:", scheduled_tasks)
        return scheduled_tasks

    def automate_maintenance(self, maintenance_tasks):
        for task in maintenance_tasks:
            print(f"Automating maintenance task: {task['description']}")
            time.sleep(1)  # Simulate time taken for maintenance
        print("All maintenance tasks automated.")
        return maintenance_tasks

# Example usage
if __name__ == "__main__":
    im = InfrastructureManagement()

    # Monitor infrastructure components
    im.monitor_component("ATC-001", "Operational")
    im.monitor_component("FAC-002", "Maintenance Required")

    # Optimize resource allocation
    resources = [
        {"id": "R1", "priority": 2},
        {"id": "R2", "priority": 1},
        {"id": "R3", "priority": 3}
    ]
    im.optimize_resource_allocation(resources)

    # Automate scheduling
    tasks = [
        {"id": "T1", "deadline": "2025-01-01"},
        {"id": "T2", "deadline": "2024-12-31"},
        {"id": "T3", "deadline": "2025-01-05"}
    ]
    im.automate_scheduling(tasks)

    # Automate maintenance
    maintenance_tasks = [
        {"id": "M1", "description": "Check runway lights"},
        {"id": "M2", "description": "Inspect fuel storage"},
        {"id": "M3", "description": "Test emergency systems"}
    ]
    im.automate_maintenance(maintenance_tasks)
