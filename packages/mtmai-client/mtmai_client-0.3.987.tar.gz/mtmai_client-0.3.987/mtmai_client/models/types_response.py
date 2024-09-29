from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.thread_form import ThreadForm


T = TypeVar("T", bound="TypesResponse")


@_attrs_define
class TypesResponse:
    """如果使用openapi 生成前端代码，缺少了某些类型，请在这里补充

    Attributes:
        thread_form (Union['ThreadForm', None, Unset]):
    """

    thread_form: Union["ThreadForm", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.thread_form import ThreadForm

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
        if thread_form is not UNSET:
            field_dict["thread_form"] = thread_form

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.thread_form import ThreadForm

        d = src_dict.copy()

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

        thread_form = _parse_thread_form(d.pop("thread_form", UNSET))

        types_response = cls(
            thread_form=thread_form,
        )

        types_response.additional_properties = d
        return types_response

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
