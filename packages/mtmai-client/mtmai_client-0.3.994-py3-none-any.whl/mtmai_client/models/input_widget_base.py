from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_widget_base_type import InputWidgetBaseType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InputWidgetBase")


@_attrs_define
class InputWidgetBase:
    """
    Attributes:
        label (str):
        id (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        placeholder (Union[None, Unset, str]):
        tooltip (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        type (Union[Unset, InputWidgetBaseType]):  Default: InputWidgetBaseType.STRING.
    """

    label: str
    id: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    placeholder: Union[None, Unset, str] = UNSET
    tooltip: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    type: Union[Unset, InputWidgetBaseType] = InputWidgetBaseType.STRING
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        label = self.label

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        placeholder: Union[None, Unset, str]
        if isinstance(self.placeholder, Unset):
            placeholder = UNSET
        else:
            placeholder = self.placeholder

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

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if placeholder is not UNSET:
            field_dict["placeholder"] = placeholder
        if tooltip is not UNSET:
            field_dict["tooltip"] = tooltip
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_placeholder(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        placeholder = _parse_placeholder(d.pop("placeholder", UNSET))

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

        _type = d.pop("type", UNSET)
        type: Union[Unset, InputWidgetBaseType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = InputWidgetBaseType(_type)

        input_widget_base = cls(
            label=label,
            id=id,
            name=name,
            placeholder=placeholder,
            tooltip=tooltip,
            description=description,
            type=type,
        )

        input_widget_base.additional_properties = d
        return input_widget_base

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
