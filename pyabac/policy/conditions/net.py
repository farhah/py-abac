"""
    Conditions relevant to networking context
"""

import ipaddress

from marshmallow import Schema, fields, post_load

from .base import ConditionBase, ConditionCreationError


class CIDRCondition(ConditionBase):
    """
        Condition that is satisfied when inquiry's IP address is in the provided CIDR.
    """
    name = "CIDR"

    def __init__(self, cidr):
        if not is_string(cidr):
            raise ConditionCreationError("Invalid argument type '{}' for network condition.".format(type(cidr)))
        self.cidr = cidr

    def is_satisfied(self, what):
        if not isinstance(what, str):
            return False
        try:
            ip = ipaddress.ip_address(what)
            net = ipaddress.ip_network(self.cidr)
        except ValueError:
            return False
        return ip in net


def is_string(value):
    return isinstance(value, str)


class CIDRConditionSchema(Schema):
    cidr = fields.String(required=True, allow_none=False)

    @post_load
    def post_load(self, data, **_):
        return CIDRCondition(**data)
