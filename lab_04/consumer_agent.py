import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ConsumerAgent(Agent):
    async def setup(self):
        print("ConsumerAgent starting...")
        self.current_load = 100
        self.add_behaviour(ConsumerBehaviour())


class ConsumerBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if not msg:
            await asyncio.sleep(1)
            return

        if msg.get_metadata("performative") != "request":
            return

        command = msg.body.strip()

        print(f"\nConsumerAgent received REQUEST: {command}")

        if command == "load_shed":
            self.agent.current_load -= 20
            print(f"Load reduced. New load: {self.agent.current_load}")

        elif command == "critical_load_reduction":
            self.agent.current_load -= 40
            print(f"Critical load reduction. New load: {self.agent.current_load}")

        else:
            print("Unknown command.")
            return

        reply = Message(to=str(msg.sender))
        reply.set_metadata("performative", "inform")
        reply.set_metadata("type", "ack")
        reply.body = f"{command}_executed"
        await self.send(reply)