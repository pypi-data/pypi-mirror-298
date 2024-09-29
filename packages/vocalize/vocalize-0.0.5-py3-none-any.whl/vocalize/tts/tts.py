from abc import ABC, abstractmethod


class TTS(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        pass

    @abstractmethod
    async def receive(self) -> bytes:
        pass
    
    @abstractmethod
    async def connect(self):
        pass
    
    @abstractmethod
    async def disconnect(self):
        pass

