import asyncio

from agents.lab03_agents import CoordinatorAgent, RescueAgent, SensorAgent
from environment.disaster_environment import DisasterEnvironment


async def run_lab_03():
    env = DisasterEnvironment()

    # Credentials as requested
    s_agent = SensorAgent("s_agentx@xmpp.jp", "pass123")
    c_agent = CoordinatorAgent("c_agentx@xmpp.jp", "pass123")
    r_agent = RescueAgent("r_agentx@xmpp.jp", "pass123")

    print("\n" + "=" * 50)
    print("      LAB 03: DISASTER RESPONSE SIMULATION")
    print("=" * 50)

    # 1. SENSOR Sensing
    report = await s_agent.sense_and_report(env, c_agent.jid)
    await asyncio.sleep(1)

    # 2. COORDINATOR Deliberating
    task = await c_agent.receive_report(report, s_agent.jid)
    await asyncio.sleep(1)

    # 3. RESCUE Acting
    if task:
        await r_agent.react_to_disaster(task)
    else:
        print("\n[SYSTEM] Simulation ended: No intervention required.")

    print("=" * 50)
    print("--- EXECUTION TRACE COMPLETE ---")
    print(f"Logs saved to: log_s_agentx.txt, log_c_agentx.txt, log_r_agentx.txt")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(run_lab_03())
    except KeyboardInterrupt:
        print("\nSimulation aborted by user.")
