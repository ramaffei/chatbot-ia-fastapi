from functools import wraps
from typing import Any
from unittest import mock

import pytest

pytest_plugins = [
    "tests.unit",
]


def get_marks(request: Any) -> list:
    return [
        x.name
        for x in next(
            (i.own_markers for i in getattr(request.node, "items", [request.node])), []
        )
    ]


@pytest.fixture(scope="session", autouse=True)
def patches(
    request: Any,
) -> None:
    # if @pytest.mark.nopatch is used, this fixture is not auto used
    if "nopatch" in get_marks(request):
        return
    patches: dict[str, Any] = {}
    patched = []
    for patch in patches:
        _mock = mock.patch(patch, return_value=patches[patch])
        _mock.start()
        patched.append(_mock)

    def teardown() -> None:
        for _patch in patched:
            _patch.stop()

    request.addfinalizer(teardown)


# We need to disable the @cache decorator during testing
def mock_cache(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)

        return inner

    return wrapper


mock.patch("fastapi_cache.decorator.cache", mock_cache).start()
