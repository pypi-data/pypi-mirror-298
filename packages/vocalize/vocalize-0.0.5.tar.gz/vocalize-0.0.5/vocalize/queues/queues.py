import asyncio
import typing


class TTSOutputQueueDict(typing.TypedDict):
    """
    Type definition for the Queue that receives from the TTS and sends to Output
    """
    text: str | None
    audio: bytes | None


TTSOutputQueue: typing.TypeAlias = asyncio.Queue[TTSOutputQueueDict | None]

