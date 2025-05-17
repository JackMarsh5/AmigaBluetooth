import asyncio
import pygame
from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.canbus.canbus_pb2 import Twist2d
from pathlib import Path
from farm_ng.core.events_file_reader import proto_from_json_file

async def main(service_config_path: Path):
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    config = proto_from_json_file(service_config_path, EventServiceConfig())
    client = EventClient(config)

    try:
        while True:
            pygame.event.pump()
            x_axis = joystick.get_axis(0)
            y_axis = -joystick.get_axis(1)

            twist = Twist2d(
                linear_velocity_x=y_axis * 1.0,
                angular_velocity=x_axis * 1.0
            )

            await client.request_reply("/twist", twist)
            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-config", type=Path, required=True)
    args = parser.parse_args()

    asyncio.run(main(args.service_config))
