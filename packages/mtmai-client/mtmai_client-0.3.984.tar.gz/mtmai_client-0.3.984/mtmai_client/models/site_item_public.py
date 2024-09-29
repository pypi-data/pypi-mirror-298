import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SiteItemPublic")


@_attrs_define
class SiteItemPublic:
    """
    Attributes:
        id (str):
        title (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        keywords (Union[None, Unset, str]):
        author (Union[None, Unset, str]):
        copyright_ (Union[None, Unset, str]):
        created_at (Union[Unset, datetime.datetime]):  Default: isoparse('2024-09-28T08:52:55.468015').
        owner_id (Union[None, Unset, str]):
    """

    id: str
    title: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    keywords: Union[None, Unset, str] = UNSET
    author: Union[None, Unset, str] = UNSET
    copyright_: Union[None, Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = isoparse("2024-09-28T08:52:55.468015")
    owner_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        keywords: Union[None, Unset, str]
        if isinstance(self.keywords, Unset):
            keywords = UNSET
        else:
            keywords = self.keywords

        author: Union[None, Unset, str]
        if isinstance(self.author, Unset):
            author = UNSET
        else:
            author = self.author

        copyright_: Union[None, Unset, str]
        if isinstance(self.copyright_, Unset):
            copyright_ = UNSET
        else:
            copyright_ = self.copyright_

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        owner_id: Union[None, Unset, str]
        if isinstance(self.owner_id, Unset):
            owner_id = UNSET
        else:
            owner_id = self.owner_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if author is not UNSET:
            field_dict["author"] = author
        if copyright_ is not UNSET:
            field_dict["copyright"] = copyright_
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_keywords(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        keywords = _parse_keywords(d.pop("keywords", UNSET))

        def _parse_author(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        author = _parse_author(d.pop("author", UNSET))

        def _parse_copyright_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        copyright_ = _parse_copyright_(d.pop("copyright", UNSET))

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_owner_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner_id = _parse_owner_id(d.pop("owner_id", UNSET))

        site_item_public = cls(
            id=id,
            title=title,
            description=description,
            keywords=keywords,
            author=author,
            copyright_=copyright_,
            created_at=created_at,
            owner_id=owner_id,
        )

        site_item_public.additional_properties = d
        return site_item_public

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
