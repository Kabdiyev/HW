from typing import Any

from fastapi import Depends, Response, status
from pydantic import Field
from fastapi.responses import JSONResponse

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
import logging


class UserShanyraksLikes(AppModel):
    id: Any = Field(alias="_id")
    address: str


class Likes(AppModel):
    shanyraks: UserShanyraksLikes


@router.get(
    "auth/users/favorites/shanyraks1/{id: str}",
    status_code=200,
)
def get_my_likes(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    result = svc.repository.get_shanyraks_by_id(jwt_data.user_id)
    logging.info(result)
    return UserShanyraksLikes(**result[0])
