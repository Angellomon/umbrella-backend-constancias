from typing import Optional
from ..db.mongodb import Database, DBSession
from ..models.users import User, UserCreate, UserDB


async def get_user(
    db: Database, /, username: str, *, session: DBSession = None
) -> Optional[User]:
    collection = db.users_collection

    user_doc = await collection.find_one({"username": username}, session=session)

    return User(**user_doc) if user_doc else None


async def get_user_db(
    db: Database,
    *,
    username: Optional[str] = None,
) -> Optional[UserDB]:
    """obtiene al usuario en base de datos con base en su username"""
    query = {}

    if username:
        query["username"] = username

    collection = db.users_collection
    user_doc = await collection.find_one(query)

    return UserDB(**user_doc) if user_doc else None


async def create_user(
    db: Database, /, user_data: UserCreate, *, session: DBSession = None
) -> User:
    collection = db.users_collection

    user_db = UserDB(**user_data.dict())
    user_db.change_password(user_data.password)

    await collection.insert_one(user_db.dict(), session=session)

    return User(**user_db.dict())


async def authenticate_user(
    db: Database,
    *,
    username: Optional[str] = None,
    password: str,
) -> Optional[User]:
    user = await get_user_db(db, username=username)

    if user and user.check_password(password):
        return User(**user.dict())
