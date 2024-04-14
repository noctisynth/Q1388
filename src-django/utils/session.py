from typing import Any
from account.models import Session, UserAccount


def verify_session(session_key: Any) -> UserAccount:
    query = Session.objects.filter(session_key=session_key)
    if query.count() != 0:
        return query[0].account
    else:
        return None  # type: ignore
