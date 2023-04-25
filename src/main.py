import time
import logging
import asyncio

# File imports
import Connector
from connections.socket_client import SocketIOClient
from module.Camera import Camera


# Main program
async def main():
    con = Connector.Connector()

    websocket_client = SocketIOClient(
        'http://localhost:3000', con)  # Test server URL

    # websocket_client = SocketIOClient('http://localhost:8080', con)  # Real server

    await websocket_client.connect()

    camera = Camera()

    if con.connected:
        try:
            while True:
                # Here you can add your logic to decide which command to send
                # Example: forward for 2 seconds, then stop
                con.forward()
                await asyncio.sleep(1)
                con.backward()
                await asyncio.sleep(1)
                con.read_data()
                logging.debug(f"Gyro: {con.get_gyro_data()}")

                camera.start_preview()
                camera.capture("test-image.jpg")
                camera.start_preview()

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
