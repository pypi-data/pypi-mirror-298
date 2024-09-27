import uuid

from fastapi import Depends

from ..utils.aws_cognito import AWSCognitoService, get_aws_cognito
from ..dto import UserDTO
from ..utils.bearer import get_token


def require_user(
        token: str = Depends(get_token),
        cognito_service: AWSCognitoService = Depends(get_aws_cognito)
) -> UserDTO:
    user_data = cognito_service.get_current_user(token)

    user_attributes = cognito_service.get_user_attributes(token)
    practice_id_str = user_attributes.get("custom:practice_id")
    practice_id = uuid.UUID(practice_id_str) if practice_id_str else None
    user_data["practice_id"] = practice_id

    return UserDTO(**user_data)
