from typing import Any
from account.models import Session


def verify_session(session_key: Any) -> bool:
    query = Session.objects.filter(session_key=session_key)
    return query.count() != 0
