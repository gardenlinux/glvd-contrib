from __future__ import annotations

from datetime import datetime
from typing import Any
from sqlalchemy import JSON, Column, DateTime, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import (
    UserDefinedType
)


class Base(DeclarativeBase):
    type_annotation_map = {
        str: Text,
        datetime: DateTime(timezone=True),
        Any: JSON
    }

# Type in Postgres:
# CREATE TYPE CVSSDATA AS (
#   version text,
#   vectorString text,
#   baseScore real
# );

class CvssData(UserDefinedType):
    cache_ok = True

    def __init__(self, version: str, vectorString: str, baseScore: float):
        self.version = version
        self.vectorString = vectorString
        self.baseScore = baseScore

    def get_col_spec(self, **kw):
        return "CVSSDATA(%s,%s,%s)" % (self.version, self.vectorString, self.baseScore)

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process


class Nist_Cve(Base):
    __tablename__ = "nist_cve"
    id: Mapped[str] = mapped_column(primary_key=True)
    cvss_severity: Mapped[str] = mapped_column(CvssData)

# Connect to the database
DATABASE_URI = f"postgresql://glvd:glvd@localhost/glvd"
engine = create_engine(DATABASE_URI, echo=True)

# Create tables in database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Insert data and issue queries
with Session(engine) as session:
    session.add(
        Nist_Cve(
            id = "CVE-123",
            cvss_severity=CvssData(version='"2.0"', vectorString='"AV:N/AC:L/Au:N/C:N/I:P/A:N"', baseScore=9.0)))
    session.commit()

    query = select(Nist_Cve)
    results = session.execute(query)
