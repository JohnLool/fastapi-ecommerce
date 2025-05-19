from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_authenticate_user_success(user_service_with_mocked_repo, monkeypatch):
    service, repo = user_service_with_mocked_repo

    async def fake_verify_password(pwd, hashed):
        return True

    monkeypatch.setattr("app.services.user_service.verify_password", fake_verify_password)

    result = await service.authenticate_user("john", "password")

    assert result.username == "john"
    repo.get_by_username.assert_called_once_with("john")

@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(user_service_with_mocked_repo, monkeypatch):
    service, repo = user_service_with_mocked_repo

    async def fake_verify_password(pwd, hashed):
        return False

    monkeypatch.setattr("app.services.user_service.verify_password", fake_verify_password)

    result = await service.authenticate_user("john", "invalid_password")

    assert result is None
    repo.get_by_username.assert_called_once_with("john")

@pytest.mark.asyncio
async def test_authenticate_user_user_not_found(user_service_user_not_found, monkeypatch):
    service, repo = user_service_user_not_found

    fake_verify_password = AsyncMock()
    monkeypatch.setattr("app.services.user_service.verify_password", fake_verify_password)

    result = await service.authenticate_user("unknown", "password")

    assert result is None
    repo.get_by_username.assert_called_once_with("unknown")
    fake_verify_password.assert_not_called()
