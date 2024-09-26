from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BotConfig")


@_attrs_define
class BotConfig:
    """mtmaibot 配置

    Attributes:
        base_url (Union[None, Unset, str]):
        api_prefix (Union[None, Unset, str]):  Default: '/api/v1'.
        access_token (Union[None, Unset, str]):
        login_url (Union[Unset, str]):  Default: '/auth/login'.
    """

    base_url: Union[None, Unset, str] = UNSET
    api_prefix: Union[None, Unset, str] = "/api/v1"
    access_token: Union[None, Unset, str] = UNSET
    login_url: Union[Unset, str] = "/auth/login"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base_url: Union[None, Unset, str]
        if isinstance(self.base_url, Unset):
            base_url = UNSET
        else:
            base_url = self.base_url

        api_prefix: Union[None, Unset, str]
        if isinstance(self.api_prefix, Unset):
            api_prefix = UNSET
        else:
            api_prefix = self.api_prefix

        access_token: Union[None, Unset, str]
        if isinstance(self.access_token, Unset):
            access_token = UNSET
        else:
            access_token = self.access_token

        login_url = self.login_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_url is not UNSET:
            field_dict["baseUrl"] = base_url
        if api_prefix is not UNSET:
            field_dict["apiPrefix"] = api_prefix
        if access_token is not UNSET:
            field_dict["accessToken"] = access_token
        if login_url is not UNSET:
            field_dict["loginUrl"] = login_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_base_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        base_url = _parse_base_url(d.pop("baseUrl", UNSET))

        def _parse_api_prefix(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_prefix = _parse_api_prefix(d.pop("apiPrefix", UNSET))

        def _parse_access_token(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        access_token = _parse_access_token(d.pop("accessToken", UNSET))

        login_url = d.pop("loginUrl", UNSET)

        bot_config = cls(
            base_url=base_url,
            api_prefix=api_prefix,
            access_token=access_token,
            login_url=login_url,
        )

        bot_config.additional_properties = d
        return bot_config

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
