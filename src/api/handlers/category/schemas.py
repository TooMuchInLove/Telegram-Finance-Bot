from marshmallow import fields

from api.schemas import CamelCaseSchema


class TelegramUserIdSchema(CamelCaseSchema):
    telegram_user_id = fields.Integer(required=True)


class AddCategoryRequestSchema(CamelCaseSchema):
    name = fields.String(required=True)


class GetCategoryResponseSchema(CamelCaseSchema):
    name = fields.String()
    created_at = fields.DateTime()


class GetCategoriesResponseSchema(CamelCaseSchema):
    items = fields.List(fields.Nested(GetCategoryResponseSchema()))
