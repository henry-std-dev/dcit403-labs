import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class PowerPlantAgent(Agent):
    async def setup(self):
        print("PowerPlantAgent starting...")
        self.add_behaviour(PowerPlantBehaviour())


class PowerPlantBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if not msg:
            await asyncio.sleep(1)
            return

        if msg.get_metadata("performative") != "request":
            return

        command = msg.body.strip()

        print(f"\nPowerPlant received REQUEST: {command}")

        if command == "increase_generation_minor":
            print("Increasing generation slightly.")

        elif command == "increase_generation_moderate":
            print("Increasing generation significantly.")

        elif command == "activate_backup":
            print("Activating backup generators.")

        elif command == "emergency_shutdown":
            print("Emergency shutdown activated.")

        else:
            print("Unknown command.")
            return

        reply = Message(to=str(msg.sender))
        reply.set_metadata("performative", "inform")
        reply.set_metadata("type", "ack")
        reply.body = f"{command}_executed"
        await self.send(reply)