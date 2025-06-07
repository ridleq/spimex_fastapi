import pytest
from main import app
from api.routers import get_session


@pytest.fixture
def override_get_session(session_mock):
    async def _override():
        yield session_mock
    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.clear()
