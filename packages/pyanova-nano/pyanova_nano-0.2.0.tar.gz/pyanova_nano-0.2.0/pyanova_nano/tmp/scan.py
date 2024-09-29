import asyncio

from bleak import BleakScanner, AdvertisementData, BLEDevice

SERVICE_UUID = "0e140000-0af1-4582-a242-773e63054c68"


async def detection_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    print(f"Found device: {device.address} - {device.name}")
    print(f"Matches service UUID: {SERVICE_UUID in advertisement_data.service_uuids}")


async def discover():
    scanner = BleakScanner(
        detection_callback=detection_callback,
        use_bdaddr=False,
        service_uuids=[SERVICE_UUID],
        bluez={"UUIDs": [SERVICE_UUID]},
    )

    devices = await scanner.find_device_by_name("Nano")
    await asyncio.sleep(20)
    print(devices)


asyncio.run(discover())
