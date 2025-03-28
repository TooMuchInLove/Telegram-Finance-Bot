from marshmallow import Schema as MarshmallowSchema


class Schema(MarshmallowSchema):
    class Meta:
        ordered = True


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation and snake-
    case for its internal representation."""

    def on_bind_field(self, field_name, field_obj) -> None:
        field_obj.data_key = camelcase(field_obj.data_key or field_name)
