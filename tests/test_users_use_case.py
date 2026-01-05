from application.use_cases.users_use_case import UsersUseCase, CreateUserDTO
from unittest.mock import patch, Mock
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import pytest
from datetime import datetime

@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_create_user_successful(user_repository_patch):
    repository = user_repository_patch.return_value
    repository.read = Mock(return_value=None)
    repository.create = Mock(return_value=True)
    
    expected_result = {"message": "User created successful"}
    use_case = UsersUseCase()
    dto_mock = Mock()
    

    status_code, result = await use_case.create_user(dto_mock)
    
    assert status_code == HTTP_201_CREATED
    assert result ==  expected_result
    

@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_create_user_internal_error(user_repository_patch):
    repository = user_repository_patch.return_value
    repository.read = Mock(return_value=None)
    repository.create = Mock(return_value="Database error")

    use_case = UsersUseCase()
    dto_mock = Mock()
    dto_mock.email = "user@example.com"

    status_code, result = await use_case.create_user(dto_mock)

    assert status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert result == {
        "message": "Database error"
    }


@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_create_user_already_exists(user_repository_patch):
    repository = user_repository_patch.return_value
    
    user_mock = Mock()
    user_mock.email = "user@example.com"

    repository.read = Mock(return_value=user_mock)

    use_case = UsersUseCase()
    dto_mock = Mock()
    dto_mock.email = "user@example.com"

    status_code, result = await use_case.create_user(dto_mock)

    assert status_code == HTTP_400_BAD_REQUEST
    assert result == {
        "message": "The user@example.com already exist"
    }


@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_read_user_not_found(user_repository_patch):
    repository = user_repository_patch.return_value
    repository.read = Mock(return_value=None)

    use_case = UsersUseCase()

    status_code, result = await use_case.read_user("user@example.com")

    assert status_code == HTTP_404_NOT_FOUND
    assert result == {"content": "User not found!"}
    

@pytest.mark.asyncio
@patch("application.use_cases.users_use_case.UsersRepository")
async def test_read_user_successful(user_repository_patch):
    repository = user_repository_patch.return_value

    claim_mock = Mock()
    claim_mock.id = 1
    claim_mock.description = "read"
    claim_mock.active = True

    user_mock = Mock()
    user_mock.id = 1
    user_mock.name = "User"
    user_mock.email = "user@example.com"
    user_mock.role_id = 1
    user_mock.created_at = datetime.utcnow()
    user_mock.updated_at = None
    user_mock.claims = [claim_mock]

    repository.read = Mock(return_value=user_mock)

    use_case = UsersUseCase()

    status_code, result = await use_case.read_user("user@example.com")

    assert status_code == HTTP_200_OK
    assert "content" in result

    dto = result["content"]

    assert dto.id == 1
    assert dto.email == "user@example.com"
    assert dto.role_id == 1
    assert len(dto.claims) == 1
    assert dto.claims[0].description == "read"

