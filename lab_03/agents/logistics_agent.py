import asyncio
import json
import random


class LogisticsAgent:
    def __init__(self, jid, password):
        self.jid = jid
        self.password = password
        self.resource_log = []

    def handle_request(self, resource_type, quantity):
        """Simulate resource allocation."""
        print(
            f"[LOGISTICS {self.jid}] Handling resource request: {resource_type}, {quantity}"
        )
        allocation = {
            "resource_type": resource_type,
            "quantity_allocated": quantity,
            "status": "Allocated",
        }
        self.resource_log.append(allocation)
        return allocation

    async def start(self, rescue_agent):
        print(f"Logistics Agent {self.jid} starting...")
        for rescue_info in rescue_agent.rescue_log:
            await asyncio.sleep(2)
            resource_type = "Medical Supplies"
            quantity = random.randint(5, 20)
            allocation = self.handle_request(resource_type, quantity)
            print(f"[LOGISTICS {self.jid}] Resource Allocation: {allocation}")

    async def stop(self):
        print(f"Logistics Agent {self.jid} stopping...")
        with open(f"logistics_log_{self.jid}.json", "w") as f:
            json.dump(self.resource_log, f, indent=2)
