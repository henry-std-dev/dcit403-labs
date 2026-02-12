import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class EchoAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Agent received: {msg.body}")
                reply = msg.make_reply()
                reply.body = f"Echo: {msg.body}"
                await self.send(reply)

    async def setup(self):
        print(f"EchoAgent starting at {self.jid}")
        print("Welcome to the Echo Agent! Waiting for messages...")

        await asyncio.sleep(5)

        print("Closing EchoAgent...")
        await self.stop()


async def main():
    # XMPP server for testing
    agent_jid = "stra_ang3r@xmpp.jp"
    agent_password = "y12$d34*!#"

    agent = EchoAgent(agent_jid, agent_password)

    await agent.start(auto_register=True)
    print("Agent started. The agent will stop after 5 seconds.")
    await asyncio.sleep(5)

    await agent.stop()
    print("Agent stopped.")


if __name__ == "__main__":
    asyncio.run(main())
