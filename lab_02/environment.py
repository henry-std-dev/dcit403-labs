import json
import random
from datetime import datetime


class DisasterEnvironment:
    def __init__(self):
        self.locations = ["Zone_A", "Zone_B", "Zone_C", "Zone_D"]
        self.event_types = ["Earthquake", "Fire", "Flood", "Structural_Collapse"]
        self.damage_levels = ["Low", "Medium", "High", "Critical"]

    def generate_event(self):
        """Generate random disaster event"""
        return {
            "timestamp": datetime.now().isoformat(),
            "location": random.choice(self.locations),
            "event_type": random.choice(self.event_types),
            "damage_level": random.choice(self.damage_levels),
            "casualties": random.randint(0, 50),
            "urgency": random.choice(["Low", "Medium", "High", "Immediate"]),
        }
