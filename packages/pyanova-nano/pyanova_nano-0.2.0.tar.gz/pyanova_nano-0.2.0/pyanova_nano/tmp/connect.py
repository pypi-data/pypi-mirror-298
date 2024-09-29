import asyncio

from bleak import BLEDevice

from pyanova_nano import PyAnova
import pyanova_nano

print(pyanova_nano.__file__)

import logging

logging.basicConfig(level=logging.INFO)


async def stop_anova():
    async with PyAnova() as client:
        # await client.connect(timeout_seconds=120)
        print(client._device.details)
        #
        print(await client.get_sensor_values())
        # await asyncio.sleep(0.5)
        print(await client.get_unit())
        #
        # await client.disconnect()


asyncio.run(stop_anova())
