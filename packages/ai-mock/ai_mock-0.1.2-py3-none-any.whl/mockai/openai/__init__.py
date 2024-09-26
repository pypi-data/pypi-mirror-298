from functools import partial
from importlib.util import find_spec

from mockai.constants import API_KEY, ENDPOINT, NOT_AVAILABLE

__all__ = [
    "OpenAI",
    "AsyncOpenAI",
    "Client",
    "AsyncClient",
]

OpenAI = NOT_AVAILABLE
AsyncOpenAI = NOT_AVAILABLE

Client = NOT_AVAILABLE
AsyncClient = NOT_AVAILABLE

if find_spec("openai"):
    from openai import (
        AsyncClient,
        AsyncOpenAI,
        Client,
        OpenAI,
    )

    OpenAI = partial(OpenAI, base_url=ENDPOINT, api_key=API_KEY)
    AsyncOpenAI = partial(AsyncOpenAI, base_url=ENDPOINT, api_key=API_KEY)

    Client = partial(Client, base_url=ENDPOINT, api_key=API_KEY)
    AsyncClient = partial(AsyncClient, base_url=ENDPOINT, api_key=API_KEY)
