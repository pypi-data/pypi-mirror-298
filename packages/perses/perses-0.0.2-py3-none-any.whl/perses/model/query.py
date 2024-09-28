from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from perses.model.common import BaseModel, DatasourceRef


class PrometheusTimeSeriesQuerySpec(BaseModel):
    query: str
    datasource: Optional[DatasourceRef] = None
    series_name_format: Optional[str] = None
    min_step: Optional[str] = None
    resolution: Optional[int] = None


class PrometheusTimeSeriesQuery(BaseModel):
    kind: Literal["PrometheusTimeSeriesQuery"] = "PrometheusTimeSeriesQuery"
    spec: PrometheusTimeSeriesQuerySpec


TimeSeriesQueryPlugin = PrometheusTimeSeriesQuery


class TimeSeriesQuerySpec(BaseModel):
    plugin: TimeSeriesQueryPlugin


class TimeSeriesQuery(BaseModel):
    kind: Literal["TimeSeriesQuery"] = "TimeSeriesQuery"
    spec: TimeSeriesQuerySpec


class TempoTraceQuerySpec(BaseModel):
    query: str
    datasource: Optional[DatasourceRef] = None


class TempoTraceQuery(BaseModel):
    kind: Literal["TempoTraceQuery"] = "TempoTraceQuery"
    spec: TempoTraceQuerySpec


TraceQueryPlugin = TempoTraceQuery


class TraceQuerySpec(BaseModel):
    plugin: TraceQueryPlugin


class TraceQuery(BaseModel):
    kind: Literal["TraceQuery"] = "TraceQuery"
    spec: TraceQuerySpec


QuerySpec = Annotated[Union[TimeSeriesQuery, TraceQuery], Field(discriminator="kind")]
