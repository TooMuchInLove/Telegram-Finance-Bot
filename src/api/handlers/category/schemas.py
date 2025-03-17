from marshmallow import fields

from src.api.schemas import CamelCaseSchema


class TelegramUserIdSchema(CamelCaseSchema):
    telegram_user_id = fields.Integer(required=True)


class CategoryRequestSchema(CamelCaseSchema):
    name = fields.String(required=True)
    category_name = fields.String(required=True)


class GetCategoryDetailResponseSchema(CamelCaseSchema):
    name = fields.String()
    created_at = fields.DateTime()


class GetCategoryResponseSchema(CamelCaseSchema):
    name = fields.String()
    account_id = fields.Integer()
    created_at = fields.DateTime()
    details = fields.List(fields.Nested(GetCategoryDetailResponseSchema()))
