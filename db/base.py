# SQLAlchemy Base - Foundation for all tables

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database table models.
    Every table in the project inherits from this.
    """
    pass