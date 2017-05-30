"""
Custom Marshmallow Fields
=========================
"""
from flask_marshmallow import base_fields


class StringList(base_fields.List):
    """
    Custom field to handle delimiter-separated lists.

    It is useful for POST parameters since they are always treated as strings.

    WARNING: It is only for use in Parameters! If you use it in Schema, the
    field will be treated as a string instead of an object! See this issue:
    https://github.com/marshmallow-code/apispec/issues/120
    """
    def __init__(self, delimiter=' ', *args, **kwargs):
        self.delimiter = delimiter
        super(StringList, self).__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data):
        """
        Converting string to a list.
        Deserializing with ``schema`` if provided
        """
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        return super(StringList, self)._deserialize(value.split(self.delimiter), attr, data)
