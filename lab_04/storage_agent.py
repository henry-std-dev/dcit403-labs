import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class StorageAgent(Agent):
    async def setup(self):
        print("StorageAgent starting...")
        self.energy_level = 100
        self.add_behaviour(StorageBehaviour())


class StorageBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if not msg:
            await asyncio.sleep(1)
            return

        if msg.get_metadata("performative") != "request":
            return

        command = msg.body.strip()

        print(f"\nStorageAgent received REQUEST: {command}")

        if command == "discharge_moderate":
            if self.agent.energy_level >= 20:
                self.agent.energy_level -= 20
                print("Moderate discharge (20 units).")

        elif command == "discharge_severe":
            if self.agent.energy_level >= 40:
                self.agent.energy_level -= 40
                print("Severe discharge (40 units).")

        elif command == "emergency_mode":
            print("Storage entering emergency mode.")

        else:
            print("Unknown command.")
            return

        reply = Message(to=str(msg.sender))
        reply.set_metadata("performative", "inform")
        reply.set_metadata("type", "ack")
        reply.body = f"{command}_executed"
        await self.send(reply)