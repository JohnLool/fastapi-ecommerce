import pytest
from unittest.mock import AsyncMock

from app.services.user_service import UserService
from app.models.user import UserOrm


@pytest.mark.asyncio
async def test_authenticate_user_success(monkeypatch):
    fake_user = UserOrm(
        id=1,
        username="john",
        hashed_password="hashed_password",
        email='john@example.com'
    )

    repo_mock = AsyncMock()
    repo_mock.get_by_username.return_value = fake_user

    async def fake_verify_password(pwd, hashed):
        return True

    monkeypatch.setattr("app.services.user_service.verify_password", fake_verify_password)

    service = UserService(db=None)
    service.repository = repo_mock

    result = await service.authenticate_user("john", "password")

    assert result == fake_user
    repo_mock.get_by_username.assert_called_once_with("john")
