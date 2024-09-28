from ..ss_session import get_current_redis_session


def get_keys(key_query: str) -> list[bytes]:
    redis_session = get_current_redis_session()
    return redis_session.keys(key_query)


def get_value(key: str) -> bytes:
    redis_session = get_current_redis_session()
    return redis_session.get(key)


def delete_key(key: str):
    redis_session = get_current_redis_session()
    redis_session.delete(key)
