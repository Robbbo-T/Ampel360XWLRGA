from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path
import uuid
import numpy as np
from sklearn.linear_model import LinearRegression

@dataclass
class UniversalDID:
    """Digital Identity for EPIC-ID system"""
    did_code: str
    access_level: str
    creation_date: datetime
    last_modified: datetime
    owner: str
    
@dataclass
class Component:
    """Aircraft component data structure"""
    section: int
    part_number: str
    description: str
    key_features: str
    primary_function: str
    technologies: str
    weight: float
    supplier: str
    compliance: Dict[str, bool]
    
class AMPEL360System:
    """Main system for managing aircraft components with EPIC-ID integration"""
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
        self.current_user: Optional[UniversalDID] = None
        self.access_log: List[Dict] = []
        self.qspace_enabled = True
        
    def authenticate_user(self, did_code: str) -> bool:
        """Authenticate user with Universal-DID"""
        # Simulated authentication
        if did_code == "HUMANPERSON.000.000.000.0.010":
            self.current_user = UniversalDID(
                did_code=did_code,
                access_level="ADMIN",
                creation_date=datetime.now(),
                last_modified=datetime.now(),
                owner="Amedeo Pelliccia"
            )
            return True
        return False
    
    def add_component(self, component_data: Dict) -> str:
        """Add new component with security check"""
        if not self.current_user:
            raise PermissionError("Authentication required")
            
        component_id = str(uuid.uuid4())
        self.components[component_id] = Component(
            section=component_data['section'],
            part_number=component_data['part_number'],
            description=component_data['description'],
            key_features=component_data['key_features'],
            primary_function=component_data['primary_function'],
            technologies=component_data['technologies'],
            weight=component_data.get('weight', 0.0),
            supplier=component_data['supplier'],
            compliance=component_data['compliance']
        )
        
        self._log_action(f"Added component {component_id}")
        return component_id
    
    def get_component(self, component_id: str) -> Optional[Component]:
        """Retrieve component with access logging"""
        if not self.current_user:
            raise PermissionError("Authentication required")
            
        component = self.components.get(component_id)
        if component:
            self._log_action(f"Retrieved component {component_id}")
        return component
    
    def export_database(self, filepath: str) -> None:
        """Export component database with EPIC-ID metadata"""
        if not self.current_user:
            raise PermissionError("Authentication required")
            
        export_data = {
            "metadata": {
                "universal_did": self.current_user.did_code,
                "export_date": datetime.now().isoformat(),
                "qspace_enabled": self.qspace_enabled
            },
            "components": {
                cid: {
                    "section": c.section,
                    "part_number": c.part_number,
                    "description": c.description,
                    "key_features": c.key_features,
                    "primary_function": c.primary_function,
                    "technologies": c.technologies,
                    "weight": c.weight,
                    "supplier": c.supplier,
                    "compliance": c.compliance
                }
                for cid, c in self.components.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        self._log_action(f"Exported database to {filepath}")
    
    def analyze_compliance(self) -> Dict:
        """Analyze component compliance status"""
        if not self.current_user:
            raise PermissionError("Authentication required")
            
        analysis = {
            "total_components": len(self.components),
            "rohs_compliant": 0,
            "itar_restricted": 0,
            "total_weight": 0.0,
            "suppliers": set()
        }
        
        for component in self.components.values():
            if component.compliance.get("RoHS", False):
                analysis["rohs_compliant"] += 1
            if component.compliance.get("ITAR", False):
                analysis["itar_restricted"] += 1
            analysis["total_weight"] += component.weight
            analysis["suppliers"].add(component.supplier)
        
        analysis["suppliers"] = list(analysis["suppliers"])
        return analysis
    
    def optimize_power_distribution(self, power_demand: List[float], power_supply: List[float]) -> List[float]:
        """Optimize power distribution using AI"""
        X = np.array(power_demand).reshape(-1, 1)
        y = np.array(power_supply).reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        optimized_distribution = model.predict(X).flatten().tolist()
        self._log_action("Optimized power distribution")
        return optimized_distribution
    
    def _log_action(self, action: str) -> None:
        """Log system actions with EPIC-ID tracking"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_did": self.current_user.did_code if self.current_user else "UNKNOWN",
            "action": action
        }
        self.access_log.append(log_entry)

def main():
    """Example usage of the AMPEL360 system"""
    system = AMPEL360System()
    
    # Authenticate user
    if system.authenticate_user("HUMANPERSON.000.000.000.0.010"):
        print("Authentication successful")
        
        # Add sample component
        component_data = {
            "section": 5,
            "part_number": "GPAM-AMPEL-0201-71-ASSY",
            "description": "Propulsion System (Q-01)",
            "key_features": "Quantum Entanglement Engine",
            "primary_function": "Thrust generation",
            "technologies": "Quantum Propulsion",
            "weight": 10000.0,
            "supplier": "QuantumPropulsion Ltd.",
            "compliance": {"RoHS": True, "ITAR": True}
        }
        
        component_id = system.add_component(component_data)
        print(f"Added component with ID: {component_id}")
        
        # Export database
        system.export_database("aircraft_database.json")
        
        # Analyze compliance
        analysis = system.analyze_compliance()
        print("\nCompliance Analysis:")
        print(f"Total Components: {analysis['total_components']}")
        print(f"RoHS Compliant: {analysis['rohs_compliant']}")
        print(f"ITAR Restricted: {analysis['itar_restricted']}")
        print(f"Total Weight: {analysis['total_weight']} kg")
        print(f"Suppliers: {', '.join(analysis['suppliers'])}")
        
        # Optimize power distribution
        power_demand = [100, 200, 300, 400, 500]
        power_supply = [90, 210, 310, 390, 510]
        optimized_distribution = system.optimize_power_distribution(power_demand, power_supply)
        print(f"Optimized Power Distribution: {optimized_distribution}")

if __name__ == "__main__":
    main()
