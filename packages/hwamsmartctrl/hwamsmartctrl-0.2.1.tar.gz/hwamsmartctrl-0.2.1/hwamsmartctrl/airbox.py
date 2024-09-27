""" API client for IHS Airboxes """
import asyncio
import sys

import aiodns
import aiohttp

from hwamsmartctrl.stovedata import StoveData, stove_data_of


class Airbox:
    """
    The combustion control unit aka HWAM® SmartControl™ or IHS Airbox.

    A HWAM stove that is smart control enabled, is equipped with a so
    called "airbox" which automatically distributes the air through 3
    valves.
    """

    ENDPOINT_GET_STOVE_DATA = "/get_stove_data"
    ENDPOINT_START = "/start"
    ENDPOINT_SET_BURN_LEVEL = "/set_burn_level"

    def __init__(self, host: str):
        """
        Parameters
        ----------
        host
            The host IP address or domain name.
        """
        self._host = host
        self._session = None
        self._base_url = f"http://{host}"

    async def __aenter__(self):
        return await self.connect()

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()

    async def connect(self):
        """ Connects to the airbox

        To close the connection call :func:`self.close`
        """
        self._session = aiohttp.ClientSession()
        return self

    async def close(self):
        """ Closes the connection """
        await self._session.close()
        self._session = None

    async def determine_hostname(self) -> str:
        """ Tries to determine the hostname of the stoves Airbox.

        This is not equal to the name set up in the iOS or Android app.
        """
        resolver = aiodns.DNSResolver(loop=asyncio.get_event_loop())
        return await resolver.gethostbyaddr(self._host)

    async def get_stove_data(self) -> StoveData:
        """ Requests all vital stove data from the Airbox.  """
        async with self._session.get(self._base_url + self.ENDPOINT_GET_STOVE_DATA) as response:
            data = await response.json(content_type="text/json")
            return stove_data_of(data)

    async def start_combustion(self) -> bool:
        """ Commands to start the combustion.

        Returns
        - - - -
        Always True because the Airbox always response with a OK.
        """
        async with self._session.get(self._base_url + self.ENDPOINT_START) as response:
            data = await response.json()
            return data["response"] == "OK"

    async def set_burn_level(self, level: int) -> bool:
        """
        Sets the burn level in the range 0-5.

        Level 0: HWAM Smart Control runs at lowest
        possible comustion temperature to maintain correct combustion
        over the longest possible time, taking into account the room
        temperature.

        Level 1-4: At these levels, the system aims
        to achieve a constant room temperature. Therefore, once you
        have found the heat level that suits you best, do not turn the
        level up and down. At level 1-4, the system starts up gently
        until it finds the right level of flue gas temperature compared
        to the desired room temperature. For normal operation, levels
        2-3 are recommended.

        Level 5: Level 5 is a booster level intended only for situations
        where the stove needs to produce a lot of heat within a short
        period of time. The stove should NOT run at level 5 for a long
        period of time. NB! If level 5 is chosen, a lot of wood is needed
        to maintain correct combustion. Therefore, re-stoking alarams may
        sound even if there are still flames and unburned wood in the
        combustion chamber.

        Throws NotImplementedError as it does work with Airbox version 3.23.0
        """
        raise NotImplementedError


async def main(host: str):
    """ Example usage of Airbox class to read stove data """
    async with Airbox(host) as stove:
        stove_data = await stove.get_stove_data()
        for key, value in stove_data.__dict__.items():
            print(f"{key} = {value}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(main(sys.argv[1]))
    else:
        print("Not enough arguments provided.")
