from aiohttp import ClientResponseError as AiohttpClientResponseError


class ClientResponseError(AiohttpClientResponseError):
    pass
