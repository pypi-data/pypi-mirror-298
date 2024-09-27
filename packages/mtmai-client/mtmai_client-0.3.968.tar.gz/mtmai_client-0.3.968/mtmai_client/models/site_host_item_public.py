from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SiteHostItemPublic")


@_attrs_define
class SiteHostItemPublic:
    """
    Attributes:
        domain (str):
        id (str):
        is_default (Union[Unset, bool]):  Default: False.
        is_https (Union[Unset, bool]):  Default: False.
    """

    domain: str
    id: str
    is_default: Union[Unset, bool] = False
    is_https: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        domain = self.domain

        id = self.id

        is_default = self.is_default

        is_https = self.is_https

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
                "id": id,
            }
        )
        if is_default is not UNSET:
            field_dict["is_default"] = is_default
        if is_https is not UNSET:
            field_dict["is_https"] = is_https

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        domain = d.pop("domain")

        id = d.pop("id")

        is_default = d.pop("is_default", UNSET)

        is_https = d.pop("is_https", UNSET)

        site_host_item_public = cls(
            domain=domain,
            id=id,
            is_default=is_default,
            is_https=is_https,
        )

        site_host_item_public.additional_properties = d
        return site_host_item_public

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
