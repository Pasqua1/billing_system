import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base(object):

    __name__: str
    metadata: MetaData
