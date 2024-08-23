from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from sqlalchemy import (
    ARRAY,
    JSON,
    Column,
    DateTime,
    String,
    Text,
    create_engine,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import (
    INT,
    TypeDecorator,
    UserDefinedType,
)

import enum
import os

@enum.verify(enum.UNIQUE)
class CvssSeverity(enum.Enum):
    NONE = 0
    UNIMPORTANT = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

    @classmethod
    def from_score(cls, score: int) -> CvssSeverity:
        if score < 0 or score > 10:
            raise ValueError
        if score >= 9:
            return cls.CRITICAL
        if score >= 7:
            return cls.HIGH
        if score >= 4:
            return cls.MEDIUM
        if score > 0:
            return cls.LOW
        return cls.NONE


class CvssSeverityType(TypeDecorator):
    cache_ok = True
    impl = INT

    def process_bind_param(self, value: CvssSeverity | None, dialect) -> int | None:
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value: int | None, dialect) -> CvssSeverity | None:
        if value is not None:
            return CvssSeverity(value)
        return None


class Base(DeclarativeBase):
    type_annotation_map = {
        str: Text,
        datetime: DateTime(timezone=True),
        Any: JSON,
        CvssSeverity: CvssSeverityType,
    }


class CvssMetricV40(Base):
    __tablename__ = "cvssMetricV40"
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    vector: Mapped[str] = mapped_column(String, nullable=True)


class CvssMetricV31(Base):
    __tablename__ = "cvssMetricV31"
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    vector: Mapped[str] = mapped_column(String, nullable=True)


class CvssMetricV30(Base):
    __tablename__ = "cvssMetricV30"
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    vector: Mapped[str] = mapped_column(String, nullable=True)


class CvssMetricV2(Base):
    __tablename__ = "cvssMetricV2"
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    vector: Mapped[str] = mapped_column(String, nullable=True)


class Metrics(Base):
    __tablename__ = "metrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    # v40 = mapped_column(Column(CvssMetricV40))
    # v31 = mapped_column(Column(CvssMetricV31))
    # v30 = mapped_column(Column(CvssMetricV30))
    # v2 = mapped_column(Column(CvssMetricV2))


class Nist_Cve(Base):
    __tablename__ = "nist_cve"
    id: Mapped[str] = mapped_column(primary_key=True)
    sourceIdentifier: Mapped[str] = mapped_column(String, nullable=True)
    vulnStatus: Mapped[str] = mapped_column(String, nullable=True)
    published: Mapped[str] = mapped_column(String, nullable=True)
    lastModified: Mapped[str] = mapped_column(String, nullable=True)
    evaluatorComment: Mapped[str] = mapped_column(String, nullable=True)
    evaluatorSolution: Mapped[str] = mapped_column(String, nullable=True)
    cisaExploitAdd: Mapped[str] = mapped_column(String, nullable=True)
    cisaActionDue: Mapped[str] = mapped_column(String, nullable=True)
    cisaRequiredAction: Mapped[str] = mapped_column(String, nullable=True)
    cisaVulnerabilityName: Mapped[str] = mapped_column(String, nullable=True)
    cveTags = Column(ARRAY(String), nullable=True)
    descriptions = Column(ARRAY(String), nullable=True)
    references = Column(ARRAY(String), nullable=True)
    cvss_severity: Mapped[Optional[CvssSeverity]] = mapped_column(nullable=True)


# Connect to the database
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
engine = create_engine(DATABASE_URI, echo=True)

# Create tables in database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Insert data and issue queries
with Session(engine) as session:
    session.add(
        Nist_Cve(
            id="CVE-123",
            vulnStatus="very bad",
            descriptions=["bla", "fasel"],
            cvss_severity=CvssSeverity.CRITICAL,
        )
    )
    session.commit()

    query = select(Nist_Cve)
    results = session.execute(query)
