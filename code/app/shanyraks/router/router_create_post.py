from fastapi import Depends, Response
from typing import List
import logging

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreatePostRequest(AppModel):
    address: str


@router.patch("/shanyraks/{id}/loc")
def upload_loc(
    _id: str,
    inpu: CreatePostRequest,
    svc: Service = Depends(get_service),
):
    result = svc.here_service.get_coordinates(inpu.address)
    logging.info(result)
    update_loc = svc.repository.update_loc(_id, {"loc": result})
    if update_loc.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)
