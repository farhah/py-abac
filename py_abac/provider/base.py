"""
    Attribute provider base class
"""

from abc import ABCMeta, abstractmethod
from typing import Dict, Optional, Any


class BaseAttributeProvider(metaclass=ABCMeta):
    """
        Base Attribute provider interface
    """
    @abstractmethod
    def get_attribute_value(self, ace: Optional[str], attribute_path: Optional[str]) -> Optional[str]:
        """
            Get attribute value for given access control element and attribute path. If
            attribute not found then returns None.

            :param ace: Access control element
            :param attribute_path: attribute path in ObjectPath format
            :return: attribute value
        """
        raise NotImplementedError


class AttributeProvider(BaseAttributeProvider):
    """
        Attribute provider interface
    """
    ace: str = ''
    attribute_path: str = ''

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        for required in ("ace", "attribute_path"):
            if not getattr(cls, required):
                raise TypeError(f"Can't instantiate class {cls.__name__} without \"{required}\" defined")

        return super(AttributeProvider, cls).__new__(cls)

    def __init__(self, attribute_values_cache: "RequestAttributeProvider.attribute_values_cache"):
        self.__attribute_values: str = ''
        self.attribute_values_cache: Dict[str, Dict[str, str]] = attribute_values_cache
        super(AttributeProvider, self).__init__()

    @property
    def attribute_values(self) -> str:
        """
            Get attribute_values from attribute_values_cache in Request
        """
        return self.attribute_values_cache[self.ace][self.attribute_path]

    @attribute_values.setter
    def attribute_values(self, value: str) -> None:
        self.__attribute_values = value
        self.attribute_values_cache[self.ace][self.attribute_path] = value
