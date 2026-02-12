import asyncio

from sensor_agent import SensorAgent


async def main():
    # Create sensor agent
    sensor = SensorAgent("stra_ang3r@xmpp.jp", "y12$d34*!#")

    await sensor.start()

    try:
        # Run for 30 seconds (6 perceptions)
        await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await sensor.stop()

        # Print summary
        print(f"\n   Sensor Report  ")
        print(f"Total events perceived: {len(sensor.event_log)}")
        print(f"Log saved to: sensor_log_sensor1.json")


if __name__ == "__main__":
    asyncio.run(main())
