from unittest.mock import AsyncMock

import pytest

from app.models import UserOrm
from app.services.user_service import UserService


@pytest.fixture
def fake_user():
    return UserOrm(
        id=1,
        username="john",
        hashed_password="hashed_password",
        email="john@example.com"
    )

@pytest.fixture
def user_service_with_mocked_repo(fake_user):
    repo_mock = AsyncMock()
    repo_mock.get_by_username.return_value = fake_user

    service = UserService(db=None)
    service.repository = repo_mock

    return service, repo_mock

@pytest.fixture
def user_service_user_not_found():
    repo_mock = AsyncMock()
    repo_mock.get_by_username.return_value = None

    service = UserService(db=None)
    service.repository = repo_mock

    return service, repo_mock