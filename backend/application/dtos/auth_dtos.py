from pydantic import BaseModel, Field


class LoginUserRequest(BaseModel):
    identifier: str = Field(..., description="The username or email of the user attempting to log in.")
    password: str = Field(..., description="The plain text password provided by the user.", min_length=1)

class LoginUserResponse(BaseModel):
    access_token: str = Field(..., description="The JWT access token for the authenticated session.")
    token_type: str = Field(default="bearer", description="The type of the token (e.g., 'bearer').")
    user: dict = Field(..., description="Basic information about the logged-in user (e.g., id, username, role).")

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="The reset token received via email.")
    new_password: str = Field(..., description="The new password for the user.", min_length=8)