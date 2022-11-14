import json
from datetime import timedelta
from typing import Any

import config
import crud
from crud import user_crud
from model.users import User
from utils import security
from utils.decorator import get_db

@get_db
def reset_password(db) -> Any:
    user = crud.user_crud.reset_password(
        db, user_id=2, password='123456'
    )
    print(user)
    return "success"