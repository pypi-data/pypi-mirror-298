import logging
from typing import Callable, Optional

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.aio.subscription import Subscription
from nats.js import JetStreamContext

from lisa.globalfit.framework.bus import EventBus
from lisa.globalfit.framework.exceptions import FrameworkError
from lisa.globalfit.framework.msg.subjects import PERSISTENT_SUBJECTS, Subject

logger = logging.getLogger(__name__)


class NatsEventBus(EventBus):
    DEFAULT_STREAM = next(iter(__name__.split(".", maxsplit=1)))
    DEFAULT_SUBJECTS = PERSISTENT_SUBJECTS

    def __init__(self, servers: list[str]) -> None:
        super().__init__()
        self.servers = servers
        self.client = Client()
        self.stream: Optional[JetStreamContext] = None
        self.subscription_handles: dict[Subject, Subscription] = {}

    async def connect(
        self, stream: str = DEFAULT_STREAM, subjects: list[Subject] = DEFAULT_SUBJECTS
    ):
        logger.debug(f"connecting to NATS: {self.servers}")
        await self.client.connect(servers=self.servers)

        logger.debug("creating jetstream context")
        # FIXME Setting a None timeout is required to perform lengthy operations (such
        # as MCMC iterations) in asynchronous subscription callbacks without being
        # timed-out by the NATS client. There might be a better way to do that.
        self.stream = self.client.jetstream(timeout=None)

        logger.debug(f"adding stream '{stream}' with subjects {subjects}")
        subject_wildcards = [s + ".>" for s in subjects]
        await self.stream.add_stream(name=stream, subjects=subject_wildcards)
        logger.debug(f"connected to NATS: {await self.stream.streams_info()}")

    async def publish(self, subject: Subject, data: bytes) -> None:
        if self.stream is None:
            raise FrameworkError("not connected to NATS")
        await self.stream.publish(subject, data)
        logger.debug(f"published {len(data)} bytes on subject {subject}")

    async def subscribe(self, subject: Subject, callback: Callable) -> None:
        if self.stream is None:
            raise FrameworkError("not connected to NATS")

        if subject in self.subscription_handles:
            msg = f"multiple subscriptions to {subject} are not supported"
            raise FrameworkError(msg)

        async def message_handler(msg: Msg):
            await callback(msg.subject, msg.data)

        subscriber = await self.stream.subscribe(subject, cb=message_handler)
        self.subscription_handles[subject] = subscriber
        logger.debug(f"got subscription from {callback.__qualname__} to '{subject}'")

    async def unsubscribe(self, subject: Subject) -> None:
        try:
            subscription = self.subscription_handles[subject]
        except KeyError as err:
            logger.warning(f"no subscription for {err}")
            return

        await subscription.unsubscribe()

    async def close(self) -> None:
        await self.client.drain()
