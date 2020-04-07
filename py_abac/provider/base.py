"""
    Attribute provider base class
"""

from abc import ABCMeta, abstractmethod
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..context import EvaluationContext
    from .request import RequestAttributeProvider


class AttributeProvider(metaclass=ABCMeta):
    """
        Attribute provider interface
    """
    __required_attrs = ['ace', 'attribute_path']

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls.__name__ != 'RequestAttributeProvider':
            for required in cls.__required_attrs:
                if not getattr(cls, required):
                    raise TypeError(f"Can't instantiate class {cls.__name__} \
                                      without \"{required}\" defined")
        return super(AttributeProvider, cls).__new__(cls)

    def __init__(self, request_attr_vals: "RequestAttributeProvider.attribute_values_cache",
                 ctx: "EvaluationContext"):
        self.__attribute_value: str = ''
        self.__request_attr_vals = request_attr_vals
        self.__ctx = ctx
        super(AttributeProvider, self).__init__()

    def find_value(self, ace, attribute_path):
        """
            Find attribute value from request attribute and all registered attribute providers
        """
        return self.__ctx.get_attribute_value(ace, attribute_path)

    @abstractmethod
    def get_attribute_value(self, ace: Optional[str] = None,
                            attribute_path: Optional[str] = None) -> Optional[str]:
        """
            Get attribute value for given access control element and attribute path. If
            attribute not found then returns None.

            :param ace: Access control element
            :param attribute_path: attribute path in ObjectPath format
            :return: attribute value
        """
        raise NotImplementedError

    @property
    def attribute_value(self) -> str:
        """
            Get attribute_values from attribute_values_cache in Request
        """
        return self.__request_attr_vals[getattr(self, "ace")][getattr(self, "attribute_path")]

    @attribute_value.setter
    def attribute_value(self, value: str) -> None:
        self.__attribute_value = value
        self.__request_attr_vals[getattr(self, "ace")][getattr(self, "attribute_path")] = value
