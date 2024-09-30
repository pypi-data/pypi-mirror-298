from abc import ABC
from typing import Union, Optional, TypeVar, Type, Any

import aiohttp
from aiohttp import ClientSession, ClientConnectorError
from aiohttp.typedefs import DEFAULT_JSON_DECODER

ModelType = TypeVar('ModelType', bound='Model')


class API(ABC):
    def __init__(
            self,
            session: ClientSession = None,
            json_loads: Any = DEFAULT_JSON_DECODER
    ):
        self.session = session
        self.json_loads = json_loads

    @staticmethod
    def powered() -> str:
        """Return an empty string."""
        return ''

    async def _get(self, url: str) -> Union[dict, None]:
        """Send a GET request to the given URL and return the response as JSON."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        try:
            async with self.session.get(url) as req:
                if req.status == 200:
                    return await req.json(loads=self.json_loads)
                return
        except ClientConnectorError:
            return

    async def _generate_model_instance(
            self,
            url: str,
            model: Type[ModelType],
            k: str = None
    ) -> Optional[ModelType]:
        """Generate a model instance from the given URL and optional keyword arguments.

        Args:
            url (str): The URL to fetch data from.
            model (Type[ModelType]): The model class to instantiate.
            k (str, optional): An optional keyword to wrap the data in a dictionary.

        Returns:
            Optional[ModelType]: A model instance.
        """
        dat = await self._get(url)
        if dat is None or not dat:
            return

        data_to_pass = {k: dat} if k else dat
        return model(**data_to_pass)

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
