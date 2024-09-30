from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ThreadUIState")


@_attrs_define
class ThreadUIState:
    """ThreadView 的UI 状态

    Attributes:
        enable_chat (Union[None, Unset, bool]):  Default: False.
        enable_scroll_to_bottom (Union[Unset, bool]):  Default: True.
        title (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        icons (Union[None, Unset, str]):
        layout (Union[None, Unset, str]):
        theme (Union[None, Unset, str]):
    """

    enable_chat: Union[None, Unset, bool] = False
    enable_scroll_to_bottom: Union[Unset, bool] = True
    title: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    icons: Union[None, Unset, str] = UNSET
    layout: Union[None, Unset, str] = UNSET
    theme: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enable_chat: Union[None, Unset, bool]
        if isinstance(self.enable_chat, Unset):
            enable_chat = UNSET
        else:
            enable_chat = self.enable_chat

        enable_scroll_to_bottom = self.enable_scroll_to_bottom

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

        icons: Union[None, Unset, str]
        if isinstance(self.icons, Unset):
            icons = UNSET
        else:
            icons = self.icons

        layout: Union[None, Unset, str]
        if isinstance(self.layout, Unset):
            layout = UNSET
        else:
            layout = self.layout

        theme: Union[None, Unset, str]
        if isinstance(self.theme, Unset):
            theme = UNSET
        else:
            theme = self.theme

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enable_chat is not UNSET:
            field_dict["enableChat"] = enable_chat
        if enable_scroll_to_bottom is not UNSET:
            field_dict["enableScrollToBottom"] = enable_scroll_to_bottom
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if icons is not UNSET:
            field_dict["icons"] = icons
        if layout is not UNSET:
            field_dict["layout"] = layout
        if theme is not UNSET:
            field_dict["theme"] = theme

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_enable_chat(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        enable_chat = _parse_enable_chat(d.pop("enableChat", UNSET))

        enable_scroll_to_bottom = d.pop("enableScrollToBottom", UNSET)

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

        def _parse_icons(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icons = _parse_icons(d.pop("icons", UNSET))

        def _parse_layout(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        layout = _parse_layout(d.pop("layout", UNSET))

        def _parse_theme(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        theme = _parse_theme(d.pop("theme", UNSET))

        thread_ui_state = cls(
            enable_chat=enable_chat,
            enable_scroll_to_bottom=enable_scroll_to_bottom,
            title=title,
            description=description,
            icons=icons,
            layout=layout,
            theme=theme,
        )

        thread_ui_state.additional_properties = d
        return thread_ui_state

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
