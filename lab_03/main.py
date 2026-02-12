import asyncio

from agents.coordinator_agent import CoordinatorAgent
from agents.logistics_agent import LogisticsAgent
from agents.rescue_agent import RescueAgent
from agents.sensor_agent import SensorAgent
from environment.disaster_environment import DisasterEnvironment


async def main():
    # Create the DisasterEnvironment instance
    environment = DisasterEnvironment()

    # Create all agents
    sensor = SensorAgent("s_agentx@xmpp.jp", "pass123", environment)
    rescue = RescueAgent("r_agentx@xmpp.jp", "pass123")
    logistics = LogisticsAgent("l_agentx@xmpp.jp", "pass123")
    coordinator = CoordinatorAgent("c_agentx@xmpp.jp", "pass123")

    # Start the agents
    await sensor.start()
    await rescue.start(sensor)
    await logistics.start(rescue)
    await coordinator.start(rescue, logistics)

    # Run the system for a while (e.g., 30 seconds)
    await asyncio.sleep(30)

    # Stop the agents
    await sensor.stop()
    await rescue.stop()
    await logistics.stop()
    await coordinator.stop()


if __name__ == "__main__":
    asyncio.run(main())
