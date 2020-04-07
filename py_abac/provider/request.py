"""
    Request attribute provider implementation
"""
from typing import Dict
from objectpath import Tree

from ..exceptions import InvalidAccessControlElementError, InvalidAttributePathError
from ..request import AccessRequest
from .base import AttributeProvider


class RequestAttributeProvider(AttributeProvider):
    """
        Request attribute provider
    """

    def __init__(self, request: AccessRequest):
        """
            Initialize attribute provider

            :param request: authorization request object
        """
        self._subject_tree = Tree(request.subject)
        self._resource_tree = Tree(request.resource)
        self._action_tree = Tree(request.action)
        self._context_tree = Tree(request.context)

        # Cache of attribute location and value pairs per access element used for quick attribute
        # value retrieval
        self.attribute_values_cache: Dict[str, Dict[str, str]] = {"subject": {},
                                                                    "resource": {},
                                                                    "action": {},
                                                                    "context": {}
                                                                 }

    def get_attribute_value(self, ace=None, attribute_path=None) -> str:
        """
            Get value for given access control element and attribute path.

            :param ace: access control element
            :param attribute_path: path to attribute in ObjectPath notation
            :param ctx: evaluation context instance
            :return: attribute value
        """
        # Validates given access control element and gets ObjectPath tree
        try:
            attribute_tree = getattr(self, "_{}_tree".format(ace))
        except AttributeError:
            raise InvalidAccessControlElementError(ace)

        # Check if attribute value stored in cache
        if attribute_path in self.attribute_values_cache[ace]:
            rvalue = self.attribute_values_cache[ace][attribute_path]
        else:
            # Attribute value not found in cache so get it from ObjectPath tree
            try:
                rvalue = attribute_tree.execute(attribute_path)
            # Broad exception needed for ObjectPath package
            except Exception:
                raise InvalidAttributePathError(attribute_path)
            # Store the obtained value in cache
            self.attribute_values_cache[ace][attribute_path] = rvalue
        return rvalue
