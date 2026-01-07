from application.dto.read_user_dto import ReadClaimDTO, ReadUserDTO
from application.use_cases.users_use_case import UsersUseCase, CreateUserDTO
from unittest.mock import patch, Mock
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
import pytest
from datetime import datetime


@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_create_user_successful(user_repository_patch):
    repository = user_repository_patch.return_value
    repository.read = Mock(return_value=([], 0))
    repository.create = Mock(return_value=True)

    expected_result = {"message": "User created successful"}
    use_case = UsersUseCase()
    use_case.users_repository = repository

    dto_mock = Mock()
    dto_mock.email = "user@example.com"

    status_code, result = await use_case.create_user(dto_mock)

    assert status_code == HTTP_201_CREATED
    assert result == expected_result


@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_create_user_internal_error(user_repository_patch):
    repository = user_repository_patch.return_value

    repository.read = Mock(return_value=([], 0))
    repository.create = Mock(return_value="Database error")

    use_case = UsersUseCase()
    use_case.users_repository = repository

    dto_mock = Mock()
    dto_mock.email = "user@example.com"

    status_code, result = await use_case.create_user(dto_mock)

    assert status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert result == {"message": "Database error"}


@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_create_user_already_exists(user_repository_patch):
    repository = user_repository_patch.return_value

    user_mock = Mock()
    user_mock.email = "user@example.com"

    repository.read = Mock(return_value=([user_mock], 1))

    use_case = UsersUseCase()
    use_case.users_repository = repository

    dto_mock = Mock()
    dto_mock.email = "user@example.com"

    status_code, result = await use_case.create_user(dto_mock)

    assert status_code == HTTP_400_BAD_REQUEST
    assert result == {"message": f"The {dto_mock.email} already exist"}


@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_read_user_success(user_repository_patch):
    repository = user_repository_patch.return_value

    user_mock = Mock()
    user_mock.role_id = 1
    user_mock.name = "benilton"
    user_mock.id = 123
    user_mock.email = "benilton@example.com"
    # Correção do erro de atributo aqui:
    user_mock.created_at = datetime(2023, 1, 1, 0, 0)
    user_mock.updated_at = datetime(2023, 1, 2, 0, 0)

    claim_mock = Mock()
    claim_mock.id = 456
    claim_mock.active = True
    claim_mock.description = "Admin access"
    user_mock.claims = [claim_mock]

    repository.read = Mock(return_value=([user_mock], 1))

    use_case = UsersUseCase()
    use_case.users_repository = repository

    email = "benilton@example.com"
    page = 1
    per_page = 10

    status_code, result = await use_case.read_user(email, page, per_page)

    assert status_code == HTTP_200_OK
    assert isinstance(result, dict)
    assert result["items"] == 1

    users_list = result["users"]
    assert isinstance(users_list, list)
    assert len(users_list) == 1

    user_dto = users_list[0]
    assert isinstance(user_dto, ReadUserDTO)
    assert user_dto.email == "benilton@example.com"
    assert user_dto.name == "benilton"
    assert user_dto.id == 123
    assert user_dto.role_id == 1

    assert isinstance(user_dto.claims, list)
    assert len(user_dto.claims) == 1

    claim_dto = user_dto.claims[0]
    assert isinstance(claim_dto, ReadClaimDTO)
    assert claim_dto.id == 456
    assert claim_dto.active is True
    assert claim_dto.description == "Admin access"
