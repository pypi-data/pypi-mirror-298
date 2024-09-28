from enum import StrEnum, unique
from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from perses.model.common import BaseModel, Calculation, Display, Unit
from perses.model.query import QuerySpec


@unique
class Sort(StrEnum):
    asc = "asc"
    desc = "desc"


@unique
class ChartMode(StrEnum):
    value = "value"
    percentage = "percentage"


@unique
class LegendMode(StrEnum):
    list = "list"
    table = "table"


@unique
class LegendPosition(StrEnum):
    bottom = "bottom"
    right = "right"


@unique
class LegendSize(StrEnum):
    small = "small"
    medium = "medium"


class Legend(BaseModel):
    position: LegendPosition
    mode: Optional[LegendMode] = None
    size: Optional[LegendSize] = None
    values: list[Calculation] = Field(default_factory=list)


@unique
class ColorMode(StrEnum):
    fixed = "fixed"
    fixed_single = "fixed-single"


class QuerySettings(BaseModel):
    query_index: int
    color_mode: ColorMode
    color_value: str = Field(pattern="^#(?:[0-9a-fA-F]{3}){1,2}$")


@unique
class PaletteMode(StrEnum):
    auto = "auto"
    categorical = "categorical"


@unique
class VisualShowPoints(StrEnum):
    auto = "auto"
    always = "always"


@unique
class VisualStack(StrEnum):
    all = "all"
    percent = "percent"


@unique
class VisualDisplay(StrEnum):
    line = "line"
    bar = "bar"


class Palette(BaseModel):
    mode: PaletteMode = PaletteMode.auto


class Visual(BaseModel):
    display: Optional[VisualDisplay] = None
    line_width: Optional[Annotated[float, Field(gte=0.25, lte=3)]] = None
    area_opacity: Optional[Annotated[float, Field(gte=0, lte=1)]] = None
    show_points: VisualShowPoints = VisualShowPoints.auto
    palette: Palette = Field(default_factory=Palette)
    point_radius: Optional[Annotated[float, Field(gte=0, lte=6)]] = None
    stack: Optional[VisualStack] = None
    connect_nulls: bool = False


class Sparkline(BaseModel):
    color: Optional[str] = None
    width: Optional[int] = None


class Format(BaseModel):
    unit: Unit
    decimal_places: Optional[int] = None
    short_values: bool = False


@unique
class ThresholdMode(StrEnum):
    percent = "percent"
    absolute = "absolute"


class ThresholdStep(BaseModel):
    value: float
    color: Optional[str] = None
    name: Optional[str] = None


class Thresholds(BaseModel):
    mode: Optional[ThresholdMode] = None
    default_color: Optional[str] = None
    steps: list[ThresholdStep] = Field(default_factory=list)


class BarChartSpec(BaseModel):
    calculation: Calculation
    format: Optional[Format] = None
    sort: Optional[Sort] = None
    mode: Optional[ChartMode] = None


class BarChart(BaseModel):
    kind: Literal["BarChart"] = "BarChart"
    spec: BarChartSpec


class GaugeChartSpec(BaseModel):
    calculation: Calculation
    format: Optional[Format] = None
    thresholds: Optional[Thresholds] = None
    max: Optional[float] = None


class GaugeChart(BaseModel):
    kind: Literal["GaugeChart"] = "GaugeChart"
    spec: GaugeChartSpec


class MarkdownSpec(BaseModel):
    text: str


class Markdown(BaseModel):
    kind: Literal["Markdown"] = "Markdown"
    spec: MarkdownSpec


class PieChartSpec(BaseModel):
    calculation: Calculation
    radius: int
    format: Optional[Format] = None
    sort: Optional[Sort] = None
    mode: Optional[ChartMode] = None
    legend: Optional[Legend] = None
    query_settings: list[QuerySettings] = Field(default_factory=list)
    visual: Visual = Field(default_factory=Visual)


class PieChart(BaseModel):
    kind: Literal["PieChart"] = "PieChart"
    spec: PieChartSpec


class StatChartSpec(BaseModel):
    calculation: Calculation
    format: Optional[Format] = None
    thresholds: Optional[Thresholds] = None
    sparkline: Optional[Sparkline] = None
    value_font_size: Optional[int] = None


class StatChart(BaseModel):
    kind: Literal["StatChart"] = "StatChart"
    spec: StatChartSpec


@unique
class TableDensity(StrEnum):
    compact = "compact"
    standard = "standard"
    comfortable = "comfortable"


@unique
class TableAlign(StrEnum):
    left = "left"
    center = "center"
    right = "right"


class TableColumnSettings(BaseModel):
    name: str = Field(min_length=1)
    header: Optional[str] = None
    header_description: Optional[str] = None
    cell_description: Optional[str] = None
    align: Optional[TableAlign] = None
    enable_sorting: bool = False
    width: Optional[int] = None
    hide: bool = False


class TableSpec(BaseModel):
    density: Optional[TableDensity] = None
    column_settings: list[TableColumnSettings] = Field(default_factory=list)


class Table(BaseModel):
    kind: Literal["Table"] = "Table"
    spec: TableSpec


class Tooltip(BaseModel):
    enable_pinning: bool = True


class YAxis(BaseModel):
    show: bool = True
    label: Optional[str] = None
    format: Optional[Format] = None
    min: Optional[float] = None
    max: Optional[float] = None


class TimeSeriesChartSpec(BaseModel):
    legend: Optional[Legend] = None
    tooltip: Tooltip = Field(default_factory=Tooltip)
    y_axis: YAxis = Field(default_factory=YAxis)
    thresholds: Optional[Thresholds] = None
    visual: Visual = Field(default_factory=Visual)
    query_settings: list[QuerySettings] = Field(default_factory=list)


class TimeSeriesChart(BaseModel):
    kind: Literal["TimeSeriesChart"] = "TimeSeriesChart"
    spec: TimeSeriesChartSpec


PanelPlugin = Annotated[
    Union[
        BarChart,
        GaugeChart,
        Markdown,
        PieChart,
        StatChart,
        Table,
        TimeSeriesChart,
    ],
    Field(discriminator="kind"),
]


class PanelSpec(BaseModel):
    plugin: PanelPlugin
    display: Display = Field(default_factory=Display)
    queries: list[QuerySpec] = Field(default_factory=list)


class Panel(BaseModel):
    kind: Literal["Panel"] = "Panel"
    spec: PanelSpec
