from datetime import date, datetime, timezone
from typing import Any

from humps import decamelize
from settings.db_settings import db_settings
from sqlalchemy import Column, MetaData, func, types
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s-%(column_0_name)s",
        "fk": "fk_%(table_name)s-%(column_0_name)s-%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    },
    schema=db_settings.DBSchema,
)


# define Custom Type based on DateTime
class DateTimeUTC(types.TypeDecorator):
    impl = types.DateTime
    LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
    cache_ok = True

    def process_bind_param(self, value: datetime | None, _: Any) -> datetime | None:
        if not value:
            return value
        if type(value) is date:
            value = datetime(
                value.year, value.month, value.day, 0, 0, 0, 0, tzinfo=timezone.utc
            )
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)
        return value.astimezone(timezone.utc)

    def process_result_value(self, value: datetime | None, _: Any) -> datetime | None:
        if not value:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


@as_declarative(metadata=meta)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return decamelize(cls.__name__)

    # Gestiona las foreigns keys para que siempre usen las del mismo schema.
    def __init_subclass__(cls, **kwargs: dict) -> None:
        super().__init_subclass__(**kwargs)
        schema = cls.metadata.schema  # type: ignore

        for _attr_name, column in cls.__dict__.items():
            if isinstance(column, Column):
                for fk in column.foreign_keys:
                    fk_str = str(fk._colspec)
                    if "." not in fk_str:  # solo si no tiene schema ya definido
                        # reemplazamos el colspec con el schema
                        fk._colspec = f"{schema}.{fk_str}"  # type: ignore

    updated_at: Mapped[DateTimeUTC] = mapped_column(
        DateTimeUTC, nullable=True, default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[DateTimeUTC] = mapped_column(
        DateTimeUTC, nullable=True, default=func.now()
    )
