from redis import Redis
from flask import current_app
from flask_session import Session


def get_current_redis_session(app=current_app) -> Redis:
    return app.config["SESSION_REDIS"]


class ServerSideSession:
    def __init__(self, app, host="127.0.0.1", port=6379, db=0):
        self.app = app
        self.host = host
        self.port = port
        self.db = db

        self.app.config["SESSION_TYPE"] = "redis"
        self.app.config["SESSION_SERIALIZATION_FORMAT"] = "json"
        self.app.config["SESSION_REDIS"] = Redis(host=host, port=port, db=db)
        Session(app)
