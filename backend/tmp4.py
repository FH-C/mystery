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
def restart(db) -> Any:
    res = crud.customer_crud.create_daily_task(
        db
    )
    print(json.loads(res))


if __name__ == '__main__':
    restart()
