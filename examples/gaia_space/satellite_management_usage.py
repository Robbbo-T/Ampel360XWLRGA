import datetime

class SatelliteManagement:
    def __init__(self):
        self.satellites = {}

    def add_satellite(self, satellite_id, orbit_params):
        self.satellites[satellite_id] = {
            "orbit_params": orbit_params,
            "health_status": "OK",
            "last_check": datetime.datetime.now()
        }
        print(f"Satellite {satellite_id} added with orbit parameters: {orbit_params}")

    def update_orbit(self, satellite_id, new_orbit_params):
        if satellite_id in self.satellites:
            self.satellites[satellite_id]["orbit_params"] = new_orbit_params
            print(f"Satellite {satellite_id} orbit updated to: {new_orbit_params}")
        else:
            print(f"Satellite {satellite_id} not found.")

    def perform_health_check(self, satellite_id):
        if satellite_id in self.satellites:
            self.satellites[satellite_id]["health_status"] = "OK"
            self.satellites[satellite_id]["last_check"] = datetime.datetime.now()
            print(f"Health check performed for satellite {satellite_id}. Status: OK")
        else:
            print(f"Satellite {satellite_id} not found.")

    def schedule_maneuver(self, satellite_id, maneuver_details):
        if satellite_id in self.satellites:
            print(f"Scheduled maneuver for satellite {satellite_id}: {maneuver_details}")
        else:
            print(f"Satellite {satellite_id} not found.")

    def manage_communication_link(self, satellite_id, link_status):
        if satellite_id in self.satellites:
            print(f"Communication link for satellite {satellite_id} is now {link_status}")
        else:
            print(f"Satellite {satellite_id} not found.")

# Example usage
if __name__ == "__main__":
    sm = SatelliteManagement()

    # Add satellites
    sm.add_satellite("SAT-001", {"altitude": 700, "inclination": 98.7})
    sm.add_satellite("SAT-002", {"altitude": 800, "inclination": 99.5})

    # Update satellite orbits
    sm.update_orbit("SAT-001", {"altitude": 705, "inclination": 98.9})

    # Perform health checks
    sm.perform_health_check("SAT-001")
    sm.perform_health_check("SAT-002")

    # Schedule maneuvers
    sm.schedule_maneuver("SAT-001", {"type": "orbit adjustment", "details": "Increase altitude by 5 km"})

    # Manage communication links
    sm.manage_communication_link("SAT-001", "active")
    sm.manage_communication_link("SAT-002", "inactive")
