from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InputWidget")


@_attrs_define
class InputWidget:
    """
    Attributes:
        id (str):
        label (str):
        initial (Union[Unset, Any]):
        tooltip (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
    """

    id: str
    label: str
    initial: Union[Unset, Any] = UNSET
    tooltip: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        label = self.label

        initial = self.initial

        tooltip: Union[None, Unset, str]
        if isinstance(self.tooltip, Unset):
            tooltip = UNSET
        else:
            tooltip = self.tooltip

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "label": label,
            }
        )
        if initial is not UNSET:
            field_dict["initial"] = initial
        if tooltip is not UNSET:
            field_dict["tooltip"] = tooltip
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        label = d.pop("label")

        initial = d.pop("initial", UNSET)

        def _parse_tooltip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tooltip = _parse_tooltip(d.pop("tooltip", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        input_widget = cls(
            id=id,
            label=label,
            initial=initial,
            tooltip=tooltip,
            description=description,
        )

        input_widget.additional_properties = d
        return input_widget

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
