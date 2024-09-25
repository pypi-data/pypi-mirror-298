from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.element_display import ElementDisplay
from ..models.element_size_type_0 import ElementSizeType0
from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="Element")


@_attrs_define
class Element:
    """
    Attributes:
        name (Union[Unset, str]):  Default: ''.
        id (Union[Unset, str]):
        chainlit_key (Union[None, Unset, str]):
        url (Union[None, Unset, str]):
        object_key (Union[None, Unset, str]):
        path (Union[None, Unset, str]):
        content (Union[File, None, Unset, str]):
        display (Union[Unset, ElementDisplay]):  Default: ElementDisplay.INLINE.
        size (Union[ElementSizeType0, None, Unset]):
        for_id (Union[None, Unset, str]):
        language (Union[None, Unset, str]):
        mime (Union[None, Unset, str]):
    """

    name: Union[Unset, str] = ""
    id: Union[Unset, str] = UNSET
    chainlit_key: Union[None, Unset, str] = UNSET
    url: Union[None, Unset, str] = UNSET
    object_key: Union[None, Unset, str] = UNSET
    path: Union[None, Unset, str] = UNSET
    content: Union[File, None, Unset, str] = UNSET
    display: Union[Unset, ElementDisplay] = ElementDisplay.INLINE
    size: Union[ElementSizeType0, None, Unset] = UNSET
    for_id: Union[None, Unset, str] = UNSET
    language: Union[None, Unset, str] = UNSET
    mime: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        chainlit_key: Union[None, Unset, str]
        if isinstance(self.chainlit_key, Unset):
            chainlit_key = UNSET
        else:
            chainlit_key = self.chainlit_key

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        object_key: Union[None, Unset, str]
        if isinstance(self.object_key, Unset):
            object_key = UNSET
        else:
            object_key = self.object_key

        path: Union[None, Unset, str]
        if isinstance(self.path, Unset):
            path = UNSET
        else:
            path = self.path

        content: Union[FileJsonType, None, Unset, str]
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, File):
            content = self.content.to_tuple()

        else:
            content = self.content

        display: Union[Unset, str] = UNSET
        if not isinstance(self.display, Unset):
            display = self.display.value

        size: Union[None, Unset, str]
        if isinstance(self.size, Unset):
            size = UNSET
        elif isinstance(self.size, ElementSizeType0):
            size = self.size.value
        else:
            size = self.size

        for_id: Union[None, Unset, str]
        if isinstance(self.for_id, Unset):
            for_id = UNSET
        else:
            for_id = self.for_id

        language: Union[None, Unset, str]
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        mime: Union[None, Unset, str]
        if isinstance(self.mime, Unset):
            mime = UNSET
        else:
            mime = self.mime

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if id is not UNSET:
            field_dict["id"] = id
        if chainlit_key is not UNSET:
            field_dict["chainlit_key"] = chainlit_key
        if url is not UNSET:
            field_dict["url"] = url
        if object_key is not UNSET:
            field_dict["object_key"] = object_key
        if path is not UNSET:
            field_dict["path"] = path
        if content is not UNSET:
            field_dict["content"] = content
        if display is not UNSET:
            field_dict["display"] = display
        if size is not UNSET:
            field_dict["size"] = size
        if for_id is not UNSET:
            field_dict["for_id"] = for_id
        if language is not UNSET:
            field_dict["language"] = language
        if mime is not UNSET:
            field_dict["mime"] = mime

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        id = d.pop("id", UNSET)

        def _parse_chainlit_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        chainlit_key = _parse_chainlit_key(d.pop("chainlit_key", UNSET))

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_object_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        object_key = _parse_object_key(d.pop("object_key", UNSET))

        def _parse_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        path = _parse_path(d.pop("path", UNSET))

        def _parse_content(data: object) -> Union[File, None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                content_type_0 = File(payload=BytesIO(data))

                return content_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset, str], data)

        content = _parse_content(d.pop("content", UNSET))

        _display = d.pop("display", UNSET)
        display: Union[Unset, ElementDisplay]
        if isinstance(_display, Unset):
            display = UNSET
        else:
            display = ElementDisplay(_display)

        def _parse_size(data: object) -> Union[ElementSizeType0, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                size_type_0 = ElementSizeType0(data)

                return size_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ElementSizeType0, None, Unset], data)

        size = _parse_size(d.pop("size", UNSET))

        def _parse_for_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        for_id = _parse_for_id(d.pop("for_id", UNSET))

        def _parse_language(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_mime(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mime = _parse_mime(d.pop("mime", UNSET))

        element = cls(
            name=name,
            id=id,
            chainlit_key=chainlit_key,
            url=url,
            object_key=object_key,
            path=path,
            content=content,
            display=display,
            size=size,
            for_id=for_id,
            language=language,
            mime=mime,
        )

        element.additional_properties = d
        return element

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
