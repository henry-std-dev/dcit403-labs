import asyncio
import datetime

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class EchoAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for a message with a timeout to keep the loop responsive
            msg = await self.receive(timeout=10)
            if msg:
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Received from {msg.sender}: {msg.body}")

                # Create and send the reply
                reply = msg.make_reply()
                reply.body = f"Echo: {msg.body}"
                await self.send(reply)
                print(f"[{timestamp}] Sent echo reply to {msg.sender}")

    async def setup(self):
        print(f"EchoAgent initializing at {self.jid}")
        self.add_behaviour(self.ReceiveBehaviour())
        print("Welcome to the Echo Agent! Status: Listening for messages...")


async def main():
    agent_jid = "stra_ang3r@xmpp.jp"
    agent_password = "y12$d34*!#"

    agent = EchoAgent(agent_jid, agent_password)

    # Start the agent and register it on the server
    await agent.start(auto_register=True)
    print("--- System Online ---")

    active_time = 15
    print(f"Agent will remain active for {active_time} seconds...")
    await asyncio.sleep(active_time)

    await agent.stop()
    print("--- System Offline: Agent stopped ---")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Manual exit triggered by user.")
