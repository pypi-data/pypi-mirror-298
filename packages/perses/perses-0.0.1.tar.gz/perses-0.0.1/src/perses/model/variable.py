from enum import StrEnum, unique
from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from perses.model.common import BaseModel, DatasourceRef, Display, ObjectMetadata


class TextVariableSpec(BaseModel):
    name: str
    value: str
    display: Display = Field(default_factory=Display)
    constant: bool = False


class TextVariable(BaseModel):
    kind: Literal["TextVariable"] = "TextVariable"
    spec: TextVariableSpec


@unique
class VariableSort(StrEnum):
    none = "none"
    alphabetical_asc = "alphabetical-asc"
    alphabetical_desc = "alphabetical-desc"
    numerical_asc = "numerical-asc"
    numerical_desc = "numerical-desc"
    alphabetical_ci_asc = "alphabetical-ci-asc"
    alphabetical_ci_desc = "alphabetical-ci-desc"


class LabelValue(BaseModel):
    value: str
    label: Optional[str] = None


class StaticListVariableSpec(BaseModel):
    values: list[Union[str, LabelValue]]


class StaticListVariable(BaseModel):
    kind: Literal["StaticListVariable"] = "StaticListVariable"
    spec: StaticListVariableSpec


class PrometheusLabelNamesVariableSpec(BaseModel):
    datasource: Optional[DatasourceRef] = None
    matchers: list[str] = Field(default_factory=list)


class PrometheusLabelNamesVariable(BaseModel):
    kind: Literal["PrometheusLabelNamesVariable"] = "PrometheusLabelNamesVariable"
    spec: PrometheusLabelNamesVariableSpec


class PrometheusLabelValuesVariableSpec(BaseModel):
    label_name: str
    datasource: Optional[DatasourceRef] = None
    matchers: list[str] = Field(default_factory=list)


class PrometheusLabelValuesVariable(BaseModel):
    kind: Literal["PrometheusLabelValuesVariable"] = "PrometheusLabelValuesVariable"
    spec: PrometheusLabelValuesVariableSpec


class PrometheusPromQLVariableSpec(BaseModel):
    expr: str
    label_name: Optional[str] = None


class PrometheusPromQLVariable(BaseModel):
    kind: Literal["PrometheusPromQLVariable"] = "PrometheusPromQLVariable"
    spec: PrometheusPromQLVariableSpec


ListVariablePlugin = Annotated[
    Union[
        StaticListVariable,
        PrometheusPromQLVariable,
        PrometheusLabelNamesVariable,
        PrometheusLabelValuesVariable,
    ],
    Field(discriminator="kind"),
]


class ListVariableSpec(BaseModel):
    name: str
    plugin: ListVariablePlugin
    display: Display = Field(default_factory=Display)
    default_value: Optional[Union[str, list[str]]] = None
    allow_all_value: bool = False
    allow_multiple: bool = False
    custom_all_value: Optional[str] = None
    capturing_regexp: Optional[str] = None
    sort: VariableSort = VariableSort.none


class ListVariable(BaseModel):
    kind: Literal["ListVariable"] = "ListVariable"
    spec: ListVariableSpec


VariableSpec = Annotated[Union[TextVariable, ListVariable], Field(discriminator="kind")]


class Variable(BaseModel):
    kind: Literal["Variable"] = "Variable"
    metadata: ObjectMetadata
    spec: VariableSpec


class GlobalVariable(BaseModel):
    kind: Literal["GlobalVariable"] = "GlobalVariable"
    metadata: ObjectMetadata
    spec: VariableSpec
