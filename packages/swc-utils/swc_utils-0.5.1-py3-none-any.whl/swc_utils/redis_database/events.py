import pickle
import threading
from flask import current_app
from functools import wraps
from swc_utils.ss_session import get_current_redis_session


def redis_event_listener(channel):
    with current_app.app_context():
        redis_client = get_current_redis_session()

        def decorator(func):
            @wraps(func)
            def wrapper(app, *args, **kwargs):
                pubsub = redis_client.pubsub()
                pubsub.subscribe(channel)

                for message in pubsub.listen():
                    if message["type"] == "message":
                        with app.app_context():
                            resp = current_app.ensure_sync(func)(pickle.loads(message["data"]))
                            resp_obj = pickle.dumps(resp)
                            redis_client.publish(f"resp-{channel}", resp_obj)

            threading.Thread(target=wrapper, args=(current_app._get_current_object(),), daemon=True).start()

        return decorator


def get_redis_data(channel, data):
    """Get data from a Redis event."""

    redis_client = get_current_redis_session()
    redis_client.publish(channel, pickle.dumps(data))

    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"resp-{channel}")

    for message in pubsub.listen():
        if message["type"] == "message":
            return pickle.loads(message["data"])
