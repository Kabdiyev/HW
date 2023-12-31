from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database
import logging

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def set_user_like(self, user_id, shanyrak_id: str):
        likes = self.get_user_likes(user_id)
        if shanyrak_id not in likes:
            likes.append(shanyrak_id)
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "likes": shanyrak_id,
                }
            },
        )

    def get_user_likes(self, user_id: str) -> list:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user["likes"] if "likes" in user else []

    def get_shanyraks_by_id(self, user_id) -> list:
        shanyrak_ids = self.get_user_likes(user_id)
        logging.info(shanyrak_ids)
        obj_shanyrak_id = [ObjectId(shanyrak_id) for shanyrak_id in shanyrak_ids]
        shanyraks = self.database["shanyraks"].find({"_id": {"$in": obj_shanyrak_id}})
        return [user for user in shanyraks]

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )
