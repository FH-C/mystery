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
def set_days(db) -> Any:
    crud.customer_crud.set_days(
        db
    )
