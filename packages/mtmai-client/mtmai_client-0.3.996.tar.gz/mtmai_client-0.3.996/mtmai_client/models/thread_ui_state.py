from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.thread_form import ThreadForm


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
        thread_form (Union['ThreadForm', None, Unset]):
    """

    enable_chat: Union[None, Unset, bool] = False
    enable_scroll_to_bottom: Union[Unset, bool] = True
    title: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    icons: Union[None, Unset, str] = UNSET
    layout: Union[None, Unset, str] = UNSET
    theme: Union[None, Unset, str] = UNSET
    thread_form: Union["ThreadForm", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.thread_form import ThreadForm

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

        thread_form: Union[Dict[str, Any], None, Unset]
        if isinstance(self.thread_form, Unset):
            thread_form = UNSET
        elif isinstance(self.thread_form, ThreadForm):
            thread_form = self.thread_form.to_dict()
        else:
            thread_form = self.thread_form

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
        if thread_form is not UNSET:
            field_dict["threadForm"] = thread_form

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.thread_form import ThreadForm

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

        def _parse_thread_form(data: object) -> Union["ThreadForm", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                thread_form_type_0 = ThreadForm.from_dict(data)

                return thread_form_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ThreadForm", None, Unset], data)

        thread_form = _parse_thread_form(d.pop("threadForm", UNSET))

        thread_ui_state = cls(
            enable_chat=enable_chat,
            enable_scroll_to_bottom=enable_scroll_to_bottom,
            title=title,
            description=description,
            icons=icons,
            layout=layout,
            theme=theme,
            thread_form=thread_form,
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
