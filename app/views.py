from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel

from .services.wg import WgService

router = APIRouter()


class CreatePeerIn(BaseModel):
    name: str


@router.post("/peers")
async def create_peer(
    _in: CreatePeerIn,
    wg_service=Depends(WgService),
) -> None:
    pass


@router.delete("/peers/{name}")
async def delete_peer(name: str = Path(...)) -> None:
    pass
