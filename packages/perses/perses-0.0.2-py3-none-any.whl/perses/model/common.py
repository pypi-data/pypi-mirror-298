from datetime import datetime
from enum import StrEnum, unique
from typing import Optional

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseModel(_BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=to_camel, populate_by_name=True)


class DatasourceRef(BaseModel):
    kind: str
    name: Optional[str] = None


class JSONRef(BaseModel):
    ref: str = Field(alias="$ref")


class ObjectMetadata(BaseModel):
    name: str
    project: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: Optional[int] = None


class Display(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hidden: bool = False


@unique
class Calculation(StrEnum):
    first = "first"
    last = "last"
    first_number = "first-number"
    last_number = "last-number"
    mean = "mean"
    sum = "sum"
    min = "min"
    max = "max"


@unique
class Unit(StrEnum):
    # time units
    milliseconds = "milliseconds"
    seconds = "seconds"
    minutes = "minutes"
    hours = "hours"
    days = "days"
    weeks = "weeks"
    months = "months"
    years = "years"
    # percent units
    percent = "percent"
    percent_decimal = "percent-decimal"
    # decimal units
    decimal = "decimal"
    # bytes units
    bytes = "bytes"
    # throughput units
    bits_per_sec = "bits/sec"
    bytes_per_sec = "bytes/sec"
    counts_per_sec = "counts/sec"
    events_per_sec = "events/sec"
    messages_per_sec = "messages/sec"
    ops_per_sec = "ops/sec"
    packets_per_sec = "packets/sec"
    reads_per_sec = "reads/sec"
    records_per_sec = "records/sec"
    requests_per_sec = "requests/sec"
    rows_per_sec = "rows/sec"
    writes_per_sec = "writes/sec"
