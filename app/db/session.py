from typing import Any, Dict

from settings.db_settings import db_settings
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


class SingletonDB:
    session_instance = None
    session_ro_instance = None

    default_engine_params: Dict = {}

    @staticmethod
    def get_conn_str() -> str:
        db_protocol = db_settings.DBProtocol
        db_user = db_settings.DBUser
        db_password = db_settings.DBPassword
        db_host = db_settings.DBHost
        db_name = db_settings.DBName
        db_conn = db_settings.DBConnectionString

        if not db_host and not db_conn:
            raise ValueError("Invalid DB connection settings")

        if db_host:
            conn_str = f"{db_protocol}://{db_user}:{db_password}@{db_host}/{db_name}"
        else:
            conn_str = db_conn

        return conn_str

    @classmethod
    def get_engine(cls, **kwargs: Any) -> Engine:
        return create_engine(cls.get_conn_str(), **kwargs)

    @classmethod
    def get_db(cls) -> sessionmaker:
        if cls.session_instance:
            return cls.session_instance

        engine = cls.get_engine(**cls.default_engine_params)
        cls.session_instance = sessionmaker(engine)
        return cls.session_instance

    @classmethod
    def get_ro_db(cls) -> sessionmaker:
        if cls.session_ro_instance:
            return cls.session_ro_instance

        engine = cls.get_engine(
            isolation_level="READ UNCOMMITTED", **cls.default_engine_params
        )
        cls.session_ro_instance = sessionmaker(
            engine, autoflush=False, autocommit=False
        )
        return cls.session_ro_instance
