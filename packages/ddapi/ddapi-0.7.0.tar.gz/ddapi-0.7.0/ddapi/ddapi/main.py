from typing import Union
from urllib.parse import quote

from .dataclass import DDPlayer, Master, Query, DMap, DDStatus, Player
from .deflt import API

__all__ = (
    "DDnetApi",
    "DDstats"
)


class DDnetApi(API):
    def __init__(self):
        super().__init__()
        self.domain = "ddnet.org"

    @staticmethod
    def powered() -> str:
        return 'ddnet.org'

    async def player(self, player_name: str) -> DDPlayer:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate_model_instance(
            f"https://{self.domain}/players/?json2={quote(player_name)}",
            DDPlayer
        )

    async def status(self) -> Union[DDStatus, None]:
        return await self._generate_model_instance(
            f"https://{self.domain}/status/json/stats.json",
            DDStatus
        )

    async def query(self, player: str) -> Union[Query, None]:
        return await self._generate_model_instance(
            f"https://{self.domain}/players/?query={quote(player)}",
            Query,
            "data"
        )

    async def master(self) -> Union[Master, None]:
        return await self._generate_model_instance(
            f"https://master1.{self.domain}/ddnet/15/servers.json",
            Master
        )

    async def map(self, map_name: str) -> Union[DMap, None]:
        return await self._generate_model_instance(
            f"https://{self.domain}/maps/?json={quote(map_name)}",
            DMap
        )


class DDstats(API):
    def __init__(self):
        super().__init__()
        self.url = "https://ddstats.tw/player/json?player={0}"

    @staticmethod
    def powered() -> str:
        return 'ddstats.tw'

    async def player(self, player_name: str) -> Player:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate_model_instance(
            self.url.format(quote(player_name)),
            Player
        )
