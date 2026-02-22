# consumer_agent.py

import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ConsumerAgent(Agent):

    async def setup(self):
        print("ConsumerAgent starting...")
        self.current_load = 100  # simulated demand
        self.add_behaviour(ConsumerBehaviour())


class ConsumerBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if not msg:
            await asyncio.sleep(1)
            return

        body = msg.body.strip()
        sender = str(msg.sender)

        # Ignore non-coordinator messages
        if "gridcoordinator@xmpp.jp" not in sender:
            return

        if body == "load_shed":
            print("\nConsumerAgent received load_shed command.")
            self.agent.current_load -= 20
            print(f"Action: Reduced consumption. New load: {self.agent.current_load}")

            reply = Message(to="gridcoordinator@xmpp.jp")
            reply.body = "ack:load_shed_executed"
            await self.send(reply)
