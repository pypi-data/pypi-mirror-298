from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ThreadUIState")


@_attrs_define
class ThreadUIState:
    """ThreadView 的UI 状态

    Attributes:
        enable_chat (Union[Unset, bool]):  Default: True.
        enable_scroll_to_bottom (Union[Unset, bool]):  Default: True.
        title (Union[Unset, str]):  Default: ''.
        description (Union[Unset, str]):  Default: ''.
        icons (Union[Unset, str]):  Default: ''.
        layout (Union[Unset, str]):  Default: ''.
        theme (Union[Unset, str]):  Default: ''.
    """

    enable_chat: Union[Unset, bool] = True
    enable_scroll_to_bottom: Union[Unset, bool] = True
    title: Union[Unset, str] = ""
    description: Union[Unset, str] = ""
    icons: Union[Unset, str] = ""
    layout: Union[Unset, str] = ""
    theme: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enable_chat = self.enable_chat

        enable_scroll_to_bottom = self.enable_scroll_to_bottom

        title = self.title

        description = self.description

        icons = self.icons

        layout = self.layout

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
        enable_chat = d.pop("enableChat", UNSET)

        enable_scroll_to_bottom = d.pop("enableScrollToBottom", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        icons = d.pop("icons", UNSET)

        layout = d.pop("layout", UNSET)

        theme = d.pop("theme", UNSET)

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
