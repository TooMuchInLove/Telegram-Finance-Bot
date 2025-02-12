from marshmallow import fields

from api.schemas import CamelCaseSchema


class SignInRequestSchema(CamelCaseSchema):
    telegram_user_id = fields.Integer(required=True)
    telegram_username = fields.String(missing=None)
