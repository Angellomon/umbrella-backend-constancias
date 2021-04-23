from typing import Optional
from ..db.mongodb import Database, DBSession
from ..models.users import User


async def get_user(
    db: Database, /, username: str, *, session: DBSession = None
) -> Optional[User]:
    collection = db.users_collection

    user_doc = await collection.find_one({"username": username}, session=None)

    return User(**user_doc) if user_doc else None
