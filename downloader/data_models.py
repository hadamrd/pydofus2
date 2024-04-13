from typing import Dict, Optional

from pydantic import BaseModel


class AssetMetaData(BaseModel):
    main: str
    beta: Optional[str] = None


class AssetModel(BaseModel):
    meta: AssetMetaData


class GameModel(BaseModel):
    name: str
    order: int
    gameId: int
    assets: AssetModel
    platforms: Dict[str, AssetMetaData]


class CytrusModel(BaseModel):
    version: int
    name: str
    games: Dict[str, GameModel]
    incomingReleasedGames: Optional[Dict[str, GameModel]] = None
