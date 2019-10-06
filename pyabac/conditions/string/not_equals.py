"""
    String not equals condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class NotEquals(StringCondition):

    def is_satisfied(self, ctx):
        if not is_string(ctx):
            return False
        if self.case_insensitive:
            return ctx.lower() != self.value.lower()
        return ctx != self.value


class NotEqualsSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotEquals(**data)
