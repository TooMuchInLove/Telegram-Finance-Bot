from marshmallow import fields

from src.api.schemas import CamelCaseSchema


class TelegramUserIdSchema(CamelCaseSchema):
    telegram_user_id = fields.Integer(required=True)


class WalletRequestSchema(CamelCaseSchema):
    name = fields.String(required=True)
    current_amount = fields.Decimal(required=True)


class GetWalletResponseSchema(CamelCaseSchema):
    name = fields.String()
    # TODO: Временное решение (переделать на Decimal)
    current_amount = fields.Float()
    account_id = fields.Integer()
    created_at = fields.DateTime()
