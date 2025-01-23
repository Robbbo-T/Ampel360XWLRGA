import datetime

class AssetMonitoring:
    def __init__(self):
        self.assets = {}

    def add_asset(self, asset_id, telemetry_params):
        self.assets[asset_id] = {
            "telemetry_params": telemetry_params,
            "status": "OK",
            "last_check": datetime.datetime.now()
        }
        print(f"Asset {asset_id} added with telemetry parameters: {telemetry_params}")

    def update_telemetry(self, asset_id, new_telemetry_params):
        if asset_id in self.assets:
            self.assets[asset_id]["telemetry_params"] = new_telemetry_params
            print(f"Asset {asset_id} telemetry updated to: {new_telemetry_params}")
        else:
            print(f"Asset {asset_id} not found.")

    def perform_health_check(self, asset_id):
        if asset_id in self.assets:
            self.assets[asset_id]["status"] = "OK"
            self.assets[asset_id]["last_check"] = datetime.datetime.now()
            print(f"Health check performed for asset {asset_id}. Status: OK")
        else:
            print(f"Asset {asset_id} not found.")

    def detect_anomalies(self, asset_id, threshold=80):
        if asset_id in self.assets:
            telemetry_params = self.assets[asset_id]["telemetry_params"]
            for param, value in telemetry_params.items():
                if value > threshold:
                    print(f"Anomaly detected in asset {asset_id}: {param} value {value} exceeds threshold {threshold}")
        else:
            print(f"Asset {asset_id} not found.")

    def generate_alerts(self, asset_id, threshold=80):
        if asset_id in self.assets:
            telemetry_params = self.assets[asset_id]["telemetry_params"]
            for param, value in telemetry_params.items():
                if value > threshold:
                    alert = f"Alert! {asset_id} {param} value {value} exceeds threshold {threshold}"
                    print(alert)
                    return alert
        else:
            print(f"Asset {asset_id} not found.")
        return None

# Example usage
if __name__ == "__main__":
    am = AssetMonitoring()

    # Add assets
    am.add_asset("SAT-001", {"temperature": 75, "battery": 90})
    am.add_asset("SAT-002", {"temperature": 85, "battery": 95})

    # Update telemetry data
    am.update_telemetry("SAT-001", {"temperature": 78, "battery": 88})

    # Perform health checks
    am.perform_health_check("SAT-001")
    am.perform_health_check("SAT-002")

    # Detect anomalies
    am.detect_anomalies("SAT-001")
    am.detect_anomalies("SAT-002")

    # Generate alerts
    am.generate_alerts("SAT-001")
    am.generate_alerts("SAT-002")
