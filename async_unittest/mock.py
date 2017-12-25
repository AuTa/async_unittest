from unittest.mock import Mock


class AsyncMock(Mock):
    """A mock of async.

    """

    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def __await__(self):
        return self.__await__()
