from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_auth_service, get_current_user
from app.schemas.auth import SignupRequest, LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    data: SignupRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.signup(data)



@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.login(data)



@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    current_user: dict = Depends(get_current_user),
):
    return None


@router.get("/protected/dashboard")
async def protected_dashboard(
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Welcome to the protected dashboard",
        "user_id": current_user["sub"],
    }