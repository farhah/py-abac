"""
    Other conditions tests
"""

import pytest
from marshmallow import ValidationError

from pyabac.conditions.others import Any
from pyabac.conditions.others import CIDR
from pyabac.conditions.others import Exists
from pyabac.conditions.others import NotExists
from pyabac.conditions.schema import ConditionSchema
from pyabac.context import EvaluationContext
from pyabac.request import Request


class TestOtherCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDR("127.0.0.0/16"), {"condition": "CIDR", "value": "127.0.0.0/16"}),
        (Exists(), {"condition": "Exists"}),
        (NotExists(), {"condition": "NotExists"}),
        (Any(), {"condition": "Any"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert ConditionSchema().dump(condition) == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDR("127.0.0.0/16"), {"condition": "CIDR", "value": "127.0.0.0/16"}),
        (Exists(), {"condition": "Exists"}),
        (NotExists(), {"condition": "NotExists"}),
        (Any(), {"condition": "Any"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = ConditionSchema().load(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition_type, data", [
        (CIDR, {"condition": "CIDR", "value": 1.0}),
    ])
    def test_create_error(self, condition_type, data):
        with pytest.raises(ValidationError):
            ConditionSchema().load(data)

    @pytest.mark.parametrize("condition, what, result", [
        (CIDR("127.0.0.0/24"), "10.0.0.0", False),
        (CIDR("127.0.0.0/24"), "127.0.0.1", True),
        (CIDR("127.0.0.0/24"), ")", False),
        (CIDR("127.0.0.0/24"), None, False),

        (Exists(), None, False),
        (Exists(), 1.0, True),

        (NotExists(), None, True),
        (NotExists(), 1.0, False),

        (Any(), None, True),
        (Any(), 1.0, True),
        (Any(), {"value": 1.0}, True),
        (Any(), [1.0, 2.0, "a"], True),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = Request(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
