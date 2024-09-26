from typing import Callable

from lisa.globalfit.framework.msg.subjects import Subject


class EventBus:
    def __init__(self) -> None:
        pass

    async def connect(self) -> None:
        pass

    async def publish(self, subject: Subject, data: bytes) -> None:
        pass

    async def subscribe(self, subject: Subject, callback: Callable) -> None:
        pass

    async def unsubscribe(self, subject: Subject) -> None:
        pass

    async def close(self) -> None:
        pass
