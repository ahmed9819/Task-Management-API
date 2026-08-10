from app.core.supabase import supabase
from app.schemas.auth import LoginRequest, SignupRequest, LoginResponse
class AuthService:

    async def signup(self, data: SignupRequest):
        """
        Sign up a new user using Supabase authentication.

        Args:
            data (SignupRequest): The signup request data containing email and password.

        Returns:
            dict: A dictionary containing the user information and session details.
        """
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })

        return response

    async def login(self, data: LoginRequest):
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password,
        })

        return LoginResponse(
         access_token=response.session.access_token,
         refresh_token=response.session.refresh_token,
         token_type=response.session.token_type,
         expires_in=response.session.expires_in,
         user={
            "id": response.user.id,
            "email": response.user.email
         }   
        )